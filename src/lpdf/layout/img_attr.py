# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImgAttr:
    """
    An image. It is never stretched. With only a width or a height, the other follows the
    image's proportions. With both, they are a maximum: the image takes the largest size
    that fits in them, and its box becomes that size, which the parent's align places. To
    put images of different shapes in slots of one size, wrap each in a frame of that size.
    With neither, the image has its natural size.
    """

    name: str
    # What the image shows, which a screen reader reads in a PDF/UA document; alt="" marks it as
    # decoration, which a reader skips. A PDF/UA document needs it on every image of the layout.
    # A document without pdfua ignores it.
    alt: str | None = None
    height: str | None = None
    # Width of the element. A length fixes it. fill, in a row, takes the width its line leaves
    # after the other children, shared equally if several on the line use fill, and never moves
    # to the next line; in a column it takes the full width.
    width: str | None = None
    font: str | None = None
    font_size: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
    paginate: str | None = None
    debug: bool | None = None
    # Puts the element, and everything in it, in an optional content group, which the viewer
    # shows or hides. print: printed, and not shown on screen. screen: shown on screen, and not
    # printed. The element keeps its room either way, so nothing moves. An element with a group
    # inside an element with another shows only where both show. Acrobat, Chrome and Firefox
    # switch the groups; Preview and Safari show everything, on screen and in print. Hidden
    # content is still in the file, where it can be selected and copied: it is not a way to keep
    # anything secret. A link in print content is drawn and does nothing, and a form field can't
    # be in print content: use a frame with a border for a box filled in by hand. With pdfa,
    # pdfua or pdfx on the output, everything shows.
    ocg: str | None = None
