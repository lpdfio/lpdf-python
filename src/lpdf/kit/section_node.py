from __future__ import annotations


class SectionNode:
    """A section node. Its children are an optional BookmarkNode that marks the section's first page, then
    LayerNodes, then at most one SectionLayout, then LayerNodes, in paint order: the layers before the layout
    paint under it, and the layers after it paint over it."""

    __slots__ = ("_attrs", "_nodes")

    def __init__(self, attrs: dict[str, str], nodes: list):
        self._attrs = attrs
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {
            "type": "section",
            "attrs": self._attrs,
            "nodes": [n.to_dict() for n in self._nodes],
        }
