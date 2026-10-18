# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EllipseAttr:
    """Attributes of the `ellipse` element in a layer."""

    rx: str
    ry: str
    # Where the ellipse's box goes, 2rx wide and 2ry high around it: its left edge, or with
    # anchor, an offset from that point of the page, where the box's matching point goes. The
    # centre is rx further in.
    x: str | None = None
    # Where the ellipse's box goes, 2rx wide and 2ry high around it: its top edge, or with
    # anchor, an offset from that point of the page, where the box's matching point goes. The
    # centre is ry further in.
    y: str | None = None
    anchor: str | None = None
    fill: str | None = None
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    # A hard-edged shadow: a copy of the shape, moved right and down by the first two lengths
    # (negative is left and up) and filled with the color, drawn under the shape. An opacity
    # from 0 to 1 after the color fades the shadow alone: "2pt 3pt #000000 0.2". There is no
    # blur. A shape with no fill shows the shadow only outside it.
    shadow: str | None = None
