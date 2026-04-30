from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegionAttr:
    pin: str
    page: str | None = None
    w: str | None = None
    debug: str | None = None
