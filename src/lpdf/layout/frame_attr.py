# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FrameAttr:
    """
    A box around a single child, which it centres. Never splits across pages: if it does not
    fit, the whole box moves to the next page.
    """

    font: str | None = None
    font_size: str | None = None
    # Space between the edge of the box and its content, written like CSS: one value for all
    # sides, two for top-bottom and left-right, three for top, left-right and bottom, four for
    # top, right, bottom and left.
    padding: str | None = None
    # Height of the box. Leave it out to size to the content. A length fixes it; fill takes what
    # is left after its siblings (shared equally if several use fill); full takes all the height
    # available. Any of these stops the box splitting across pages.
    height: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
    debug: str | None = None
    width: str | None = None
