from __future__ import annotations

from .canvas_node import CanvasNode


class ImageNode(CanvasNode):
    __slots__ = ("_x", "_y", "_w", "_h", "_name", "_anchor")

    def __init__(self, x: float, y: float, w: float, h: float, name: str, anchor: str | None = None):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._name = name
        self._anchor = anchor

    def to_dict(self) -> dict:
        attrs: dict = {
            "x": str(self._x), "y": str(self._y),
            "w": str(self._w), "h": str(self._h),
            "name": self._name,
        }
        if self._anchor is not None:
            attrs["anchor"] = self._anchor
        return {"type": "canvas-img", "attrs": attrs}
