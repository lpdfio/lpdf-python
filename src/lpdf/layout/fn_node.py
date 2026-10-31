from __future__ import annotations

from typing import Any

from .node import Node


class FnNode(Node):
    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "fn",
            "attrs": self._attrs,
            "nodes": [n.to_dict() if isinstance(n, Node) else n for n in self._nodes],
        }
