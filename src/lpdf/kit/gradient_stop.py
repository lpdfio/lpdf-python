from __future__ import annotations

from typing import TypedDict


class GradientStop(TypedDict):
    """One color of a gradient: ``color`` is hex, ``cmyk()``, ``rgb()``, ``hsl()`` or a color token.

    It sits at an ``offset`` from ``0%`` to ``100%``. The stops of a gradient are all CMYK or all RGB.
    """

    offset: str
    color: str
