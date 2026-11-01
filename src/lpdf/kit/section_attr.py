from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class SectionAttr:
    """Attributes for the ``section`` (page) element. ``bleed`` is how far this section's pages reach past their trim
    edge, such as ``"5mm"``: it overrides the document's, and ``"0mm"`` takes it away."""

    size: str | None = None
    orientation: str | None = None
    background: str | None = None
    title: str | None = None
    debug: bool | None = None
    type: str | None = None
    toc_indent_step: str | None = None
    footnote_counter: str | None = None
    bleed: str | None = None
