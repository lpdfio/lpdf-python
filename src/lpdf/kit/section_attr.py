from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SectionAttr:
    size: str | None = None
    orientation: str | None = None
    background: str | None = None
    title: str | None = None
    debug: str | None = None
    type: str | None = None
    toc_indent_step: str | None = None
