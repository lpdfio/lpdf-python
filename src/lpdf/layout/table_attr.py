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

    # Column widths, separated by spaces, in fr, pt or % units: for example 2fr 1fr 120pt 20%.
    cols: str
    border: str | None = None
    stripe: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
    width: str | None = None
    height: str | None = None
    debug: str | None = None
