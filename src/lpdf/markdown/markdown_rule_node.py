from __future__ import annotations


class MarkdownRuleNode:
    """A rule of a markdown's styles: the element it is named after, with the attributes it sets."""

    __slots__ = ("_type", "_attrs")

    def __init__(self, type: str, attrs: dict[str, str]):
        self._type = type
        self._attrs = attrs

    def to_dict(self) -> dict:
        return {
            "type": self._type,
            "attrs": self._attrs,
        }
