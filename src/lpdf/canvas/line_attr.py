# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LineAttr:
    """Attributes of the `line` element on the canvas."""

    x1: str
    y1: str
    x2: str
    y2: str
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    line_cap: str | None = None
