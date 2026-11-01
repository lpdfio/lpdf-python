# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MarkdownLiAttr:
    """
    An item of a bullet or a numbered list. indent is the width of the marker's column and
    bullet the shape of a bullet list's marker, as on a list; gap goes between the blocks of
    an item.
    """

    font: str | None = None
    font_size: str | None = None
    color: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    indent: str | None = None
    bullet: str | None = None
