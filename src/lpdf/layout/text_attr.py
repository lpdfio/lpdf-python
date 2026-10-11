# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextAttr:
    """
    A block of wrapping text. Use span children to style parts of it. Splits across pages
    between lines.
    """

    font_size: str | None = None
    font: str | None = None
    # Use the bold face of the font. It applies to the 14 built-in fonts: Helvetica becomes
    # Helvetica-Bold, Times-Roman becomes Times-Bold, Courier becomes Courier-Bold, and the
    # oblique and italic faces their bold forms. A custom font has no bold face to pick, so name
    # one in font.
    bold: str | None = None
    color: str | None = None
    align: str | None = None
    width: str | None = None
    # The fewest lines of the text that may stand alone at the top of the next page when it
    # splits. Default 2. If fewer would be left, lines move from the first page to the next; 1
    # turns the protection off.
    widows: str | None = None
    # The fewest lines of the text that may stand alone at the bottom of a page when it splits.
    # Default 2. If fewer would fit, the whole text moves to the next page; 1 turns the
    # protection off. When no split can keep both widows and orphans, even on an empty page, the
    # text splits where the lines fit.
    orphans: str | None = None
    paginate: str | None = None
    debug: str | None = None
