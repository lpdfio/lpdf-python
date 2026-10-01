# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CanvasImgAttr:
    """Attributes of the `img` element on the canvas."""

    name: str
    w: str
    h: str
    x: str | None = None
    y: str | None = None
    anchor: str | None = None
