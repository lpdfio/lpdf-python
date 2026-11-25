from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .chart_value_node import ChartValueNode


class ChartCategoryNode:
    """A category of a chart: a value for each series, and its label."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list[ChartValueNode]):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {"type": "category", "attrs": self._attrs, "nodes": [node.to_dict() for node in self._nodes]}
