# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from typing import TypedDict


class GradientStop(TypedDict):
    """One color of a gradient, at an offset along it."""

    # Where the color is reached along the gradient, from 0% (the start) to 100% (the end).
    # Stops go in increasing order.
    offset: str
    # The color at the stop: hex, cmyk(), rgb(), hsl(), a color token, or a spot color or a tint
    # of it. The stops of a gradient are all CMYK, all RGB, or all tints of one spot color.
    color: str
