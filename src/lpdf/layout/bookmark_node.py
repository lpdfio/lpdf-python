from __future__ import annotations

from typing import Any

from .node import Node


class BookmarkNode(Node):
    """An entry of the PDF's outline and a target for href="#id" links. It marks the node that follows it;
    directly in a section's nodes, it marks the section's first page."""

    __slots__ = ("_attrs",)

    def __init__(self, attrs: dict[str, Any]):
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {
            "type": "bookmark",
            "attrs": self._attrs,
        }
