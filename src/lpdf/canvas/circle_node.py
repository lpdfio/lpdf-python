from __future__ import annotations

from .canvas_node import CanvasNode


class CircleNode(CanvasNode):
    """A `circle` on the canvas."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "circle", "attrs": self._attrs}
