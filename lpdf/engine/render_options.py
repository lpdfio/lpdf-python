from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderOptions:
    """Per-call options for PdfEngine.render()."""
    created_on: str | None = None
    data: dict | None = None