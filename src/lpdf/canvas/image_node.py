from __future__ import annotations

from .canvas_node import CanvasNode


class ImageNode(CanvasNode):
    """An `img` on the canvas."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "img", "attrs": self._attrs}
