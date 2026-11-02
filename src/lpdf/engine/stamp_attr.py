from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class StampAttr:
    """
    One stamp for ``PdfEngine.stamp``: a PNG, the pages it goes on, and the box it is drawn in on each. The box is
    placed as a layer element is, and the image is fitted in it without distortion.
    """

    # The PNG's bytes. The same bytes object given to several stamps is embedded in the PDF once.
    image: bytes
    # The pages: a page scope, such as 3, 1-2, last, each, odd or 1,3,5-last. A page the PDF doesn't have is an error.
    page: str
    # Where the box goes, in pt, mm or in: its top-left corner, from the page's top-left corner as a viewer shows it,
    # or with anchor, signed offsets from that point of the page. Required without anchor.
    x: str | None = None
    y: str | None = None
    # The point of the page the box is placed from, and the point of the box that goes there: top-left, top-center,
    # top-right, center-left, center, center-right, bottom-left, bottom-center or bottom-right.
    anchor: str | None = None
    # The size of the box, in pt, mm or in.
    width: str
    height: str
    # Where the image sits across the box, in the room it leaves: start, center (the default) or end.
    align: str | None = None
    # Where the image sits down the box, in the room it leaves: start, center (the default) or end.
    justify: str | None = None
    # How the image is sized in the box, keeping its proportions: fit (the default) shrinks an image larger than the
    # box and keeps a smaller one at its natural size, from the resolution the PNG records, or a pixel to a point;
    # fill takes the largest size that fits.
    scale: str | None = None
    # How many times its natural size fit may grow an image, never past the box: 1, the default, or more.
    max_grow: float | None = None
