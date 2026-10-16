from __future__ import annotations

from .canvas_node import CanvasNode


class RectNode(CanvasNode):
    """A `rect` in a layer."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "rect", "attrs": self._attrs}
