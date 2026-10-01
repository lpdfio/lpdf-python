from __future__ import annotations

from .canvas_node import CanvasNode


class LayerNode(CanvasNode):
    """A canvas layer containing canvas primitives."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, str], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "layer",
            "attrs": self._attrs,
            "nodes": [n.to_dict() for n in self._nodes],
        }
