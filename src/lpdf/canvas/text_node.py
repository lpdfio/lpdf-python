from __future__ import annotations

from ..shared.attrs_helper import node_to_dict
from .canvas_node import CanvasNode


class CanvasTextNode(CanvasNode):
    """Text on the canvas. Its content is strings and `span` nodes, as in a layout `text`."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, str], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "text",
            "attrs": self._attrs,
            "nodes": [node_to_dict(n) for n in self._nodes],
        }
