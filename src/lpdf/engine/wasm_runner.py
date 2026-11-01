from __future__ import annotations

import json
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import ClassVar

import wasmtime

from .engine_exception import EngineException

DEFAULT_TIMEOUT = 30
"""The seconds a render may run when ``timeout`` is left out. A timeout of 0 means no limit."""

# One thread advances the engine's epoch at this pace, and a render's deadline is its timeout in ticks, plus one: the
# render starts between two ticks, and without it would stop up to a tick before its limit. The epoch belongs to the
# engine, not to a store, so a timer per render would stop every other render too.
_TICK_SECONDS = 0.1
_TICKS_PER_SECOND = 10

# The deadline of a render with no limit. A store's deadline is 0 until it is set, which stops it at the first tick.
_NO_DEADLINE = 2**62


def _advance_epoch(engine: wasmtime.Engine) -> None:
    # Each tick is due at a time of the clock, not a sleep after the last one, so the ticks don't drift: 300 sleeps
    # of 0.1 s took 30.8 s.
    due = time.monotonic()
    while True:
        due += _TICK_SECONDS
        time.sleep(max(0.0, due - time.monotonic()))
        engine.increment_epoch()


def _seconds(count: int) -> str:
    return f"{count} second" if count == 1 else f"{count} seconds"


def _details(files: Path) -> str:
    """What the engine wrote to stderr, for an error message."""
    text = (files / "stderr.txt").read_text(errors="replace").strip()
    return f" Stderr: {text}" if text else ""


class WasmRunner:
    """Runs the engine's WASI binary inside this process with the ``wasmtime`` package, one request per call.

    The Wasmtime engine, the compiled module and the thread that advances the epoch are made on the first render of
    the process, not at import, so a server that forks its workers makes them in each worker. Every runner and thread
    after it shares them, and each render gets a store of its own. The call into WebAssembly releases the GIL, so
    renders on threads run in parallel.
    """

    _lock: ClassVar[threading.Lock] = threading.Lock()
    _pid: ClassVar[int | None] = None
    _engine: ClassVar[wasmtime.Engine | None] = None
    _linker: ClassVar[wasmtime.Linker | None] = None
    _modules: ClassVar[dict[str, wasmtime.InstancePre]] = {}

    def __init__(self, wasm_binary: str, timeout: int | None = None):
        """:param wasm_binary: The path of the engine's WASI binary.
        :param timeout: The seconds a render may run before it stops with an ``EngineException``: 30 when left out,
            no limit at 0."""
        self._binary = wasm_binary
        self._timeout = DEFAULT_TIMEOUT if timeout is None else timeout

    def invoke(self, payload: dict) -> dict:
        """Send a request to the engine and return its response.

        :raises EngineException: when the engine reports an error, fails, or runs past the timeout.
        """
        response = json.loads(self._run(json.dumps(payload).encode()))
        if "error" in response:
            raise EngineException(f"lpdf render error: {response['error']}")
        return response

    def _run(self, request: bytes) -> bytes:
        engine, instance_pre = self._compiled()
        # WASI reads stdin only from a file or from this process's own stdin, so the request goes through a file. The
        # response and the engine's messages come back through files too: Wasmtime calls a Python callback for them
        # on threads of its own, and one that runs while Python exits aborts the process. A temp file left behind
        # must not fail a render that worked.
        with tempfile.TemporaryDirectory(prefix="lpdf-", ignore_cleanup_errors=True) as folder:
            files = Path(folder)
            (files / "request.json").write_bytes(request)
            return self._call(engine, instance_pre, files)

    def _call(self, engine: wasmtime.Engine, instance_pre: wasmtime.InstancePre, files: Path) -> bytes:
        wasi = wasmtime.WasiConfig()
        wasi.stdin_file = files / "request.json"
        wasi.stdout_file = str(files / "response.json")
        wasi.stderr_file = str(files / "stderr.txt")

        store = wasmtime.Store(engine)
        try:
            store.set_wasi(wasi)
            store.set_epoch_deadline(self._timeout * _TICKS_PER_SECOND + 1 if self._timeout > 0 else _NO_DEADLINE)
            start = instance_pre.instantiate(store).exports(store)["_start"]
            assert isinstance(start, wasmtime.Func), "a WASI command exports _start as a function"
            start(store)
        except wasmtime.ExitTrap as exited:
            if exited.code != 0:
                raise EngineException(f"The engine exited with code {exited.code}.{_details(files)}") from exited
        except wasmtime.Trap as trap:
            if trap.trap_code == wasmtime.TrapCode.INTERRUPT:
                raise EngineException(f"The render timed out after {_seconds(self._timeout)}.") from trap
            raise EngineException(f"The engine failed: {trap.message}{_details(files)}") from trap
        finally:
            # The store holds the render's memory: it goes when the render ends, not when the collector gets to it.
            store.close()

        response = (files / "response.json").read_bytes()
        if not response:
            raise EngineException(f"The engine returned no response.{_details(files)}")
        return response

    def _compiled(self) -> tuple[wasmtime.Engine, wasmtime.InstancePre]:
        """The process's engine and this runner's binary compiled on it, made on first use."""
        cls = WasmRunner
        with cls._lock:
            # A forked process has a copy of the engine, but not the thread that advances its epoch.
            if cls._pid != os.getpid():
                config = wasmtime.Config()
                config.epoch_interruption = True
                engine = wasmtime.Engine(config)
                linker = wasmtime.Linker(engine)
                linker.define_wasi()
                threading.Thread(target=_advance_epoch, args=(engine,), name="lpdf-epoch", daemon=True).start()
                cls._engine, cls._linker, cls._modules, cls._pid = engine, linker, {}, os.getpid()

            assert cls._engine is not None and cls._linker is not None, "set together with _pid above"
            instance_pre = cls._modules.get(self._binary)
            if instance_pre is None:
                try:
                    module = wasmtime.Module.from_file(cls._engine, self._binary)
                except (OSError, wasmtime.WasmtimeError) as e:
                    raise EngineException(f"Cannot load the engine binary '{self._binary}': {e}") from e
                instance_pre = cls._linker.instantiate_pre(module)
                cls._modules[self._binary] = instance_pre
            return cls._engine, instance_pre
