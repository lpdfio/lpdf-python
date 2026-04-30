from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrAttr:
    background: str | None = None
