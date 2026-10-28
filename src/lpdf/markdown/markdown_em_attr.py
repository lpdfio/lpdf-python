# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownEmAttr:
    """
    Emphasis, written *text* in Markdown. Italic in a built-in font; an embedded font names
    its italic face in font.
    """

    font: str | None = None
    color: str | None = None
