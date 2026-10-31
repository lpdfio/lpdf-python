from __future__ import annotations

from typing import Any


class MarkdownStylesNode:
    """The rules that say how the parts of a markdown look, with a file of them in ``src`` when it has one."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, Any], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "markdown-styles",
            "attrs": self._attrs,
            "nodes": [n.to_dict() for n in self._nodes],
        }
