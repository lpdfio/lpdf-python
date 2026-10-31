from __future__ import annotations

from typing import Any

from .node import Node


class BarcodeNode(Node):
    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {
            "type": "barcode",
            "attrs": self._attrs,
        }
