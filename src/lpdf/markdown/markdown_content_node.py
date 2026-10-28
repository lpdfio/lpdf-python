from __future__ import annotations


class MarkdownContentNode:
    """The Markdown itself, as strings that make one text."""

    __slots__ = ("_nodes",)

    def __init__(self, nodes: list[str]):
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "markdown-content",
            "attrs": {},
            "nodes": list(self._nodes),
        }
