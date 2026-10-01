# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegionAttr:
    """
    Pins content to the top or bottom edge of pages, outside the normal flow, for headers
    and footers. It reserves that space on every page it appears on. Only allowed directly
    inside layout, and one per pin on a page.
    """

    # Which edge the region sticks to. top and bottom work. left and right pass validation but
    # are not implemented yet.
    pin: str
    # Which pages show the region: each, first, last, odd, even, or a range such as 2-last.
    # Defaults to each.
    page: str | None = None
    w: str | None = None
    debug: str | None = None
