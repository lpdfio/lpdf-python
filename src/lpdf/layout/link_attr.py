# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinkAttr:
    """Attributes of the `link` element."""

    # Where the link goes: a URL, or #id to jump to the bookmark with that id. In an entry of a
    # table of contents, # alone jumps to that entry's bookmark.
    href: str
    gap: str | None = None
    # Width of the element. A length fixes it. fill, in a row, takes the width its line leaves
    # after the other children, shared equally if several on the line use fill, and never moves
    # to the next line; in a column it takes the full width.
    width: str | None = None
    height: str | None = None
    debug: str | None = None
