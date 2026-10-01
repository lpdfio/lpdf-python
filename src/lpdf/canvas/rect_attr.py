# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RectAttr:
    """Attributes of the `rect` element on the canvas."""

    w: str
    h: str
    x: str | None = None
    y: str | None = None
    anchor: str | None = None
    radius: str | None = None
    fill: str | None = None
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    opacity: str | None = None
