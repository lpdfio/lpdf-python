from __future__ import annotations


class ChartValueNode:
    """A value of a category, as plain text: a number, or nothing for no value."""

    __slots__ = ("_nodes",)

    def __init__(self, nodes: list[str]):
        self._nodes = nodes

    def to_dict(self) -> dict:
        return {"type": "value", "attrs": {}, "nodes": list(self._nodes)}
