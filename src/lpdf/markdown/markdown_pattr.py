# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownPAttr:
    """A paragraph, and the words of a list item, a quote and a footnote."""

    font: str | None = None
    font_size: str | None = None
    bold: str | None = None
    color: str | None = None
    align: str | None = None
    line_height: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
