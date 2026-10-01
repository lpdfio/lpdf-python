# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpanAttr:
    """Attributes of the `span` element."""

    font: str | None = None
    bold: str | None = None
    color: str | None = None
    href: str | None = None
    underline: str | None = None
    strike: str | None = None
