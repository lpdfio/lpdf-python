from __future__ import annotations

from typing import TypedDict


class GradientStop(TypedDict):
    """One color of a gradient: ``color`` is hex or a color token, at an ``offset`` from ``0%`` to ``100%``."""

    offset: str
    color: str
