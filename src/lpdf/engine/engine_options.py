from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MAX_MEMORY_MB = 1024
"""The megabytes a render may allocate when ``max_memory_mb`` is left out."""

_MOST_MEMORY_MB = 4096
"""The most ``max_memory_mb`` may be: 32-bit WebAssembly addresses 4 GB at most."""


@dataclass(frozen=True, kw_only=True)
class EngineOptions:
    """Construction-time configuration for LpdfEngine.

    ``wasm_binary`` is the path of the engine's WASI binary, the one the SDK ships when left out. ``timeout`` is the
    seconds a render may run before it stops with an ``EngineException``: 5 when left out, no limit at 0.
    ``max_memory_mb`` is the megabytes of memory a render may allocate, its data included, before it stops with an
    ``EngineException`` that names the cap: 1024 when left out, from 1 to 4096.

    :raises ValueError: when ``max_memory_mb`` is not a whole number from 1 to 4096.
    """
    wasm_binary: str | None = None
    timeout: int | None = None
    max_memory_mb: int | None = None

    def __post_init__(self) -> None:
        mb = self.max_memory_mb
        if mb is not None and (isinstance(mb, bool) or not isinstance(mb, int) or not 1 <= mb <= _MOST_MEMORY_MB):
            raise ValueError(f"max_memory_mb must be a whole number of megabytes from 1 to {_MOST_MEMORY_MB}, not {mb}")
