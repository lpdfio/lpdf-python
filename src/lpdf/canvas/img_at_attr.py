# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImgAtAttr:
    """
    An image at a fixed place on the page. It needs width or height, and the other follows
    the image's proportions. With both, they are a maximum: the image takes the largest size
    that fits in them, and its box becomes that size, so an anchor places the image itself.
    x and y place its box: the top-left corner, or with anchor, an offset from that point of
    the page, where the box's matching point goes.
    """

    name: str
    x: str | None = None
    y: str | None = None
    anchor: str | None = None
    width: str | None = None
    height: str | None = None
