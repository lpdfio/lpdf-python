# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrAttr:
    """Attributes of the `tr` element."""

    # with-next keeps the row on the same page as the row after it. A run of rows that each say
    # with-next, and the row that ends it, move to the next page together when a page break
    # would fall inside them. A run taller than a page breaks where its rows fit, as if it had
    # no keep. Rows are never split, and a header is never left alone at the bottom of a page,
    # with or without this.
    keep: str | None = None
    background: str | None = None
