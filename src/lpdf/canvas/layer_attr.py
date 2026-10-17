# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayerAttr:
    """
    Draws shapes at exact positions on the page, independent of the flowing layout:
    watermarks, stamps, page furniture. Coordinates start at the top left corner of the
    whole page, not inside the layout's margin, and y grows downward. A layer before the
    section's layout paints under it, and one after paints over it. It sets what applies to
    all of its shapes: which pages they appear on, opacity, transform and clip. Layers
    cannot be nested.
    """

    page: str | None = None
    opacity: str | None = None
    transform: str | None = None
    clip: str | None = None
