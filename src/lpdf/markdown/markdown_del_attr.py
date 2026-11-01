# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MarkdownDelAttr:
    """Struck-through text, written ~~text~~ in Markdown."""

    font: str | None = None
    color: str | None = None
    strike: bool | None = None
