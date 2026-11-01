# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MarkdownAAttr:
    """A link, written [text](url) in Markdown."""

    font: str | None = None
    color: str | None = None
    bold: bool | None = None
    underline: bool | None = None
