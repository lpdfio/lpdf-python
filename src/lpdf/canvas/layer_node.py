from __future__ import annotations

from typing import Any

from .canvas_node import CanvasNode


class LayerNode(CanvasNode):
    """A layer, which goes directly in a section, holding the shapes, text and images drawn at fixed places."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "layer",
            "attrs": self._attrs,
            "nodes": [n.to_dict() for n in self._nodes],
        }
