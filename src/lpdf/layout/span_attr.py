# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpanAttr:
    """Attributes of the `span` element."""

    font: str | None = None
    bold: bool | None = None
    color: str | None = None
    # Makes the span a link: a URL, or #id to jump to the bookmark with that id. In an entry of
    # a table of contents, # alone jumps to that entry's bookmark.
    href: str | None = None
    underline: bool | None = None
    strike: bool | None = None
