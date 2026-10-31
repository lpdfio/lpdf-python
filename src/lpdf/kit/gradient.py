# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from typing import Required, TypedDict

from .gradient_stop import GradientStop

# A named blend of colors. A background or a fill uses it as gradient:name, and the blend spans the
# box it fills. Give from and to for two colors, or stop children for more.
# The functional form, because ``from`` is a Python keyword.
Gradient = TypedDict(
    "Gradient",
    {
        # linear runs along a line across the box. radial runs from the center out to the
        # farthest corner.
        "type": Required[str],
        # The first color: hex, cmyk(), rgb(), hsl() or a color token, CMYK if to is and RGB
        # if it is not. Used with to, when there are no stop children. For a radial gradient
        # it is the center.
        "from": str,
        # The last color: hex, cmyk(), rgb(), hsl() or a color token. Used with from, when
        # there are no stop children. For a radial gradient it is the edge.
        "to": str,
        # The direction of a linear gradient, in degrees: 0 runs from the top to the bottom,
        # 90 from the left to the right, 180 from the bottom to the top. Default 0. A radial
        # gradient has no direction.
        "angle": float,
        # The colors of the gradient, for more than two: each at an offset, in increasing
        # order. Give these, or from and to.
        "stops": "list[GradientStop]",
    },
    total=False,
)
