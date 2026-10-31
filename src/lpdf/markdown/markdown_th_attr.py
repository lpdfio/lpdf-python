# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownThAttr:
    """A cell of a table's header row."""

    font: str | None = None
    font_size: str | None = None
    bold: bool | None = None
    color: str | None = None
    align: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
