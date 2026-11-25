from __future__ import annotations

from typing import Any

from .node import Node


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


class ChartSeriesNode:
    """A series of a chart: its label and color in the legend."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "series", "attrs": self._attrs}


class ChartCategoryNode:
    """A category of a chart: a value for each series, and its label."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list[ChartValueNode]):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {"type": "category", "attrs": self._attrs, "nodes": [node.to_dict() for node in self._nodes]}


class ChartValueNode:
    """A value of a category, as plain text: a number, or nothing for no value."""

    __slots__ = ("_nodes",)

    def __init__(self, nodes: list[str]):
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {"type": "value", "attrs": {}, "nodes": list(self._nodes)}
