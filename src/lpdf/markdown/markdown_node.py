from __future__ import annotations


class MarkdownNode:
    """A markdown inside a section, where a layout would go: it holds only Markdown, in its styles and its
    content."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, str], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "markdown",
            "attrs": self._attrs,
            "nodes": [n.to_dict() for n in self._nodes],
        }
