# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinkAttr:
    """Attributes of the `link` element."""

    href: str
    gap: str | None = None
    width: str | None = None
    height: str | None = None
    debug: str | None = None
