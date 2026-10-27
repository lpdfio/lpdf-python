# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownTableAttr:
    """
    A table. Its columns are sized by their content: a column takes the width its cells need
    on one line, the room that is left is shared in proportion, and a name that does not fit
    breaks at the edge of its cell. stripe is the color of every other row, or none;
    head-border is the line under the header row and row-border the line under each of the
    other rows, as thickness and color like border, or none. The default styles draw a line
    under the header in the line color and lines between the rows in line-muted, with no
    stripe.
    """

    border: str | None = None
    stripe: str | None = None
    head_border: str | None = None
    row_border: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
