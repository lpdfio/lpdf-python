"""The engine runs inside the process on the ``wasmtime`` package: renders on threads, the timeout as an epoch
deadline, and the request's temp file. A render that runs long is a small WebAssembly module of the test's own, given
as the engine's binary: the real engine renders the largest fixture in well under a second."""

import hashlib
import tempfile
import threading
import time
from pathlib import Path

import pytest
import wasmtime

from lpdf import EngineException, EngineOptions, PdfEngine, RenderOptions

from .snapshot_helper import FIXTURES, HAS_FIXTURES, SNAPSHOTS

needs_fixtures = pytest.mark.skipif(not HAS_FIXTURES, reason="fixture files not available outside the monorepo")

SPIN_FOREVER = '(module (func (export "_start") (loop $spin (br $spin))))'

RESPONSE = '{"pdf": "JVBERi0="}'
RESPONSE_IN_WAT = RESPONSE.replace('"', '\\"')

# Spins on the monotonic clock for two seconds, then writes a response that holds the bytes "%PDF-".
SPIN_TWO_SECONDS = f'''
(module
  (import "wasi_snapshot_preview1" "clock_time_get" (func $clock (param i32 i64 i32) (result i32)))
  (import "wasi_snapshot_preview1" "fd_write" (func $write (param i32 i32 i32 i32) (result i32)))
  (memory (export "memory") 1)
  (data (i32.const 32) "{RESPONSE_IN_WAT}")
  (func (export "_start")
    (local $until i64)
    (drop (call $clock (i32.const 1) (i64.const 1) (i32.const 0)))
    (local.set $until (i64.add (i64.load (i32.const 0)) (i64.const 2000000000)))
    (loop $spin
      (drop (call $clock (i32.const 1) (i64.const 1) (i32.const 0)))
      (br_if $spin (i64.lt_u (i64.load (i32.const 0)) (local.get $until))))
    (i32.store (i32.const 16) (i32.const 32))
    (i32.store (i32.const 20) (i32.const {len(RESPONSE)}))
    (drop (call $write (i32.const 1) (i32.const 16) (i32.const 1) (i32.const 24)))))
'''


def _binary(tmp_path: Path, wat: str) -> str:
    path = tmp_path / "engine.wasm"
    path.write_bytes(wasmtime.wat2wasm(wat))
    return str(path)


def _render_fixture(name: str, engine: PdfEngine | None = None) -> str:
    """The SHA-256 of a fixture rendered as the snapshot tests render it."""
    xml = (FIXTURES / f"{name}.xml").read_text(encoding="utf-8")
    engine = engine or PdfEngine()
    pdf = engine.set_license_key("test-key").render(xml, RenderOptions(skip_encryption=True))
    return hashlib.sha256(pdf).hexdigest()


def _snapshot(name: str) -> str:
    return (SNAPSHOTS / f"{name}.pdf.sha256").read_text().strip()


def _timed_render(engine: PdfEngine) -> tuple[float, Exception | None]:
    start = time.monotonic()
    try:
        engine.render("<lpdf/>")
    except EngineException as e:
        return time.monotonic() - start, e
    return time.monotonic() - start, None


@needs_fixtures
def test_two_renders_on_two_threads_at_once_both_give_the_right_hash() -> None:
    barrier = threading.Barrier(2)
    hashes: dict[str, str] = {}

    def render(name: str) -> None:
        barrier.wait()
        hashes[name] = _render_fixture(name)

    threads = [threading.Thread(target=render, args=(name,)) for name in ("bench_l", "bench_m")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert hashes == {"bench_l": _snapshot("bench_l"), "bench_m": _snapshot("bench_m")}


def test_a_render_past_its_timeout_throws_naming_the_limit(tmp_path: Path) -> None:
    engine = PdfEngine(EngineOptions(wasm_binary=_binary(tmp_path, SPIN_TWO_SECONDS), timeout=1))

    elapsed, error = _timed_render(engine)

    assert isinstance(error, EngineException)
    assert str(error) == "The render timed out after 1 second."
    assert 1 <= elapsed < 1.5


def test_a_render_with_a_timeout_of_0_runs_with_no_limit(tmp_path: Path) -> None:
    engine = PdfEngine(EngineOptions(wasm_binary=_binary(tmp_path, SPIN_TWO_SECONDS), timeout=0))

    elapsed, error = _timed_render(engine)

    assert error is None
    assert elapsed >= 2


def test_a_render_stops_after_30_seconds_when_the_timeout_is_left_out(tmp_path: Path) -> None:
    engine = PdfEngine(EngineOptions(wasm_binary=_binary(tmp_path, SPIN_FOREVER)))

    elapsed, error = _timed_render(engine)

    assert str(error) == "The render timed out after 30 seconds."
    assert 30 <= elapsed < 30.5


@needs_fixtures
def test_a_render_past_its_timeout_leaves_the_others_and_the_next_render_right(tmp_path: Path) -> None:
    """The Wasmtime engine and its epoch are the process's, shared by every PdfEngine: a render stopped at its
    deadline stops nothing else, and leaves the engine rendering right."""
    spinning = PdfEngine(EngineOptions(wasm_binary=_binary(tmp_path, SPIN_FOREVER), timeout=1))
    barrier = threading.Barrier(2)
    results: dict[str, object] = {}

    def time_out() -> None:
        barrier.wait()
        _, results["error"] = _timed_render(spinning)
        results["stopped"] = time.monotonic()

    def render_meanwhile() -> None:
        barrier.wait()
        results["hash"] = _render_fixture("bench_m", PdfEngine(EngineOptions(timeout=1)))
        results["rendered"] = time.monotonic()

    threads = [threading.Thread(target=time_out), threading.Thread(target=render_meanwhile)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert str(results["error"]) == "The render timed out after 1 second."
    assert results["hash"] == _snapshot("bench_m")
    assert results["rendered"] < results["stopped"]
    assert _render_fixture("bench_m", PdfEngine(EngineOptions(timeout=1))) == _snapshot("bench_m")


@pytest.fixture
def requests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The folder the request files of the test's renders go to."""
    folder = tmp_path / "requests"
    folder.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(folder))
    return folder


def test_the_request_file_is_removed_after_a_render(requests: Path) -> None:
    PdfEngine().render('<lpdf version="1"><document><section><layout><text>x</text></layout></section></document></lpdf>')

    assert list(requests.iterdir()) == []


def test_the_request_file_is_removed_after_a_timeout(tmp_path: Path, requests: Path) -> None:
    _, error = _timed_render(PdfEngine(EngineOptions(wasm_binary=_binary(tmp_path, SPIN_FOREVER), timeout=1)))

    assert isinstance(error, EngineException)
    assert list(requests.iterdir()) == []


def test_a_binary_that_cannot_be_read_throws_naming_it(tmp_path: Path) -> None:
    missing = str(tmp_path / "missing.wasm")

    with pytest.raises(EngineException, match="Cannot load the engine binary '.*missing.wasm'"):
        PdfEngine(EngineOptions(wasm_binary=missing)).render("<lpdf/>")
