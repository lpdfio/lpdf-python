# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class BookmarkAttr:
    """
    An entry of the PDF's outline, the bookmark panel of a viewer, and a target for links
    with href="#id" and for cross-references with bookmark-ref. It draws nothing and marks
    the element that follows it, so it is never left at the bottom of a page apart from that
    element. Directly inside a section, it marks the section's first page.
    """

    # The text of the entry, in the outline and in a table of contents.
    label: str
    # Depth in the outline, 1 to 6. Defaults to 1. An entry nests under the closest entry before
    # it with a lower level.
    level: int | None = None
    # The name links use to jump here, as href="#id", and cross-references as bookmark-ref="id".
    # Leave it out to make it from the label: lowercase, with other characters than letters and
    # digits turned into hyphens, and -2, -3 added when an earlier bookmark has it. Two
    # bookmarks may not have the same id.
    id: str | None = None
    # true leaves the bookmark out of the viewer's outline and out of the table of contents, for
    # a figure or a table: label="Table 3" ref-only="true". Links with href="#id" and
    # cross-references with bookmark-ref still reach it, and {bookmark-label} still shows its
    # label. Defaults to false.
    ref_only: bool | None = None
