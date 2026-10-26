# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownTableAttr:
    """A table. The columns share the width equally."""

    border: str | None = None
    stripe: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
