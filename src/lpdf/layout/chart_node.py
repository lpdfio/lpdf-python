from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .node import Node

if TYPE_CHECKING:
    from .chart_category_node import ChartCategoryNode
    from .chart_series_node import ChartSeriesNode


class ChartNode(Node):
    """A chart: its attributes, then its series and its categories."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list[ChartSeriesNode | ChartCategoryNode]):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "chart",
            "attrs": self._attrs,
            "nodes": [node.to_dict() for node in self._nodes],
        }
