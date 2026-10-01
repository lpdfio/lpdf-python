# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EllipseAttr:
    """Attributes of the `ellipse` element on the canvas."""

    rx: str
    ry: str
    cx: str | None = None
    cy: str | None = None
    anchor: str | None = None
    fill: str | None = None
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    opacity: str | None = None
