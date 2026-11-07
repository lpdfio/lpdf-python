# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MarkdownHrAttr:
    """
    A thematic break, written --- in Markdown: a divider. color is the color of the line and
    thickness its thickness, a length or a name from the border row of the tokens.
    """

    color: str | None = None
    thickness: str | None = None
