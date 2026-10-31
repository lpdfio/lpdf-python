from __future__ import annotations

from typing import Any

from .node import Node


class FieldNode(Node):
    """A form field leaf node. attrs must include 'type' and 'name'."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        if "type" not in attrs or not attrs["type"]:
            raise ValueError("FieldNode requires a 'type' attr")
        if "name" not in attrs or not attrs["name"]:
            raise ValueError("FieldNode requires a 'name' attr")
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {
            "type": "field",
            "attrs": self._attrs,
        }
