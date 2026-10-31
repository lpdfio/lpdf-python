from __future__ import annotations

from typing import Any

from .canvas_node import CanvasNode


class EllipseNode(CanvasNode):
    """An `ellipse` in a layer."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "ellipse", "attrs": self._attrs}
