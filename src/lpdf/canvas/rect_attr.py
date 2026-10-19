# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RectAttr:
    """Attributes of the `rect` element in a layer."""

    width: str
    height: str
    x: str | None = None
    y: str | None = None
    anchor: str | None = None
    radius: str | None = None
    fill: str | None = None
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    # A hard-edged shadow: a copy of the shape, moved right and down by the first two lengths
    # (negative is left and up) and filled with the color, drawn under the shape. An opacity
    # from 0 to 1 after the color fades the shadow alone: "2pt 3pt #000000 0.2". There is no
    # blur. A shape with no fill shows the shadow only outside it.
    shadow: str | None = None
