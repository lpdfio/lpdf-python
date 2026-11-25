from __future__ import annotations

from typing import Any


class ChartSeriesNode:
    """A series of a chart: its label and color in the legend."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "series", "attrs": self._attrs}
