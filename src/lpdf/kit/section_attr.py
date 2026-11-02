from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class SectionAttr:
    """Attributes for the ``section`` (page) element. ``bleed`` is how far this section's pages reach past their trim
    edge, such as ``"5mm"``: it overrides the document's, and ``"0mm"`` takes it away.

    ``page_start`` is the number of the section's first page, which starts a new run of pages: ``1`` restarts the
    count. ``page_format`` is how its page numbers are written, as a list's ``format`` is, such as ``"lower-roman"``, and
    ``page_prefix`` the text before them, such as ``"A-"``. A section that sets none of the three carries on the count,
    the format and the prefix of the one before. ``{page}`` prints a page's number, and ``{pages}`` how many pages its
    run has."""

    size: str | None = None
    orientation: str | None = None
    background: str | None = None
    title: str | None = None
    debug: bool | None = None
    type: str | None = None
    toc_indent_step: str | None = None
    footnote_counter: str | None = None
    bleed: str | None = None
    page_start: int | None = None
    page_format: str | None = None
    page_prefix: str | None = None
