# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CircleAttr:
    """Attributes of the `circle` element in a layer."""

    r: str
    # Where the circle's box goes, the square of side 2r around it: its left edge, or with
    # anchor, an offset from that point of the page, where the box's matching point goes. The
    # centre is r further in.
    x: str | None = None
    # Where the circle's box goes, the square of side 2r around it: its top edge, or with
    # anchor, an offset from that point of the page, where the box's matching point goes. The
    # centre is r further in.
    y: str | None = None
    anchor: str | None = None
    fill: str | None = None
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
