from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineOptions:
    """Construction-time configuration for LpdfEngine.

    ``wasm_binary`` is the path of the engine's WASI binary, the one the SDK ships when left out. ``timeout`` is the
    seconds a render may run before it stops with an ``EngineException``: 30 when left out, no limit at 0.
    """
    wasm_binary: str | None = None
    timeout: int | None = None
