from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinkAttr:
    url: str | None = None
    gap: str | None = None
    width: str | None = None
    height: str | None = None
