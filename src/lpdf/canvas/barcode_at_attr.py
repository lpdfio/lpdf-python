# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BarcodeAtAttr:
    """
    A barcode at a fixed place on the page. A QR code takes width or height. A code128 or
    ean13 needs a width. x and y place its box: the top-left corner, or with anchor, an
    offset from that point of the page, where the box's matching point goes.
    """

    type: str
    data: str
    # Height of the whole barcode, with the digits of hrt inside it: they take the bottom 12pt
    # and the bars the rest. A QR code is square: it takes width or height, and the smaller when
    # both are set. Without a height, code128 has bars 40pt high, and 12pt more with hrt, and
    # ean13 is 60pt high.
    height: str | None = None
    ec: str | None = None
    hrt: str | None = None
    color: str | None = None
    background: str | None = None
    x: str | None = None
    y: str | None = None
    anchor: str | None = None
    width: str | None = None
