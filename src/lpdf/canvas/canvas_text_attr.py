# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CanvasTextAttr:
    """
    Text at an exact position on the page: either x and y, or an anchor with optional
    offsets.
    """

    x: str | None = None
    y: str | None = None
    anchor: str | None = None
    font: str | None = None
    font_size: str | None = None
    color: str | None = None
    align: str | None = None
    w: str | None = None
    line_height: str | None = None
    opacity: str | None = None
