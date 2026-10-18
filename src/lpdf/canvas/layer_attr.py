# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayerAttr:
    """
    Draws shapes, text, images and barcodes at exact positions on the page, independent of
    the flowing layout: watermarks, stamps, page furniture. Coordinates start at the top
    left corner of the whole page, not inside the layout's margin, and y grows downward. A
    layer before the section's layout paints under it, and one after paints over it. It sets
    what applies to all of its content: which pages it appears on, opacity, transform and
    clip, and the font, size and color of its text. Layers cannot be nested.
    """

    page: str | None = None
    # How opaque everything in the layer is, from 0 to 1. To fade one element, put it in a layer
    # of its own.
    opacity: str | None = None
    transform: str | None = None
    # A rectangle that cuts off what the layer draws outside it: x y w h, in points from the top
    # left corner of the page.
    clip: str | None = None
    # The font of the text-at in the layer that sets none of its own. Defaults to the font of
    # the document.
    font: str | None = None
    # The size of the text-at in the layer that sets none of its own. Defaults to 11pt.
    font_size: str | None = None
    # The color of the text-at in the layer that sets none of its own. Defaults to the text
    # token.
    color: str | None = None
