from __future__ import annotations

from .canvas_node import CanvasNode


class BarcodeAtNode(CanvasNode):
    """A `barcode-at` in a layer."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, str]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {"type": "barcode-at", "attrs": self._attrs}
