# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TableAttr:
    """
    Rows and cells in columns whose widths are set by cols. The thead row repeats at the top
    of every page, and rows move between pages whole.
    """

    # Column widths, separated by spaces, in fr, pt or % units, or auto: for example 2fr 1fr
    # 120pt 20%. An auto column takes the width its cells need on one line, and the auto columns
    # share what the pt and % columns leave, in proportion to what they need. When they do not
    # fit, each keeps at least its longest word, and when not even those fit, the longest are
    # cut and a short column keeps its width. auto and fr cannot be in one table: use pt or %
    # for the fixed columns. For example auto 90pt 60pt.
    cols: str
    # A grid: a line around every cell, as thickness and color, for example 1pt #cccccc.
    border: str | None = None
    # The background of every other row below the header, or none.
    stripe: str | None = None
    # The line under the header row, across the table, as thickness and color like border, or
    # none: for example xs line.
    head_border: str | None = None
    # The line under each row, across the table, as thickness and color like border, or none:
    # for example xs line-muted. Under the header row, head-border takes its place when it is
    # set. A line stops where a cell spans on into the next row.
    row_border: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
    # Width of the element. A length fixes it. fill, in a row, takes the width its line leaves
    # after the other children, shared equally if several on the line use fill, and never moves
    # to the next line; in a column it takes the full width.
    width: str | None = None
    height: str | None = None
    paginate: str | None = None
    debug: bool | None = None
