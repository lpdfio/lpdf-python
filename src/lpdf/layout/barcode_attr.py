# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BarcodeAttr:
    """Attributes of the `barcode` element."""

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
    # Width of the element. A length fixes it. fill, in a row, takes the width its line leaves
    # after the other children, shared equally if several on the line use fill, and never moves
    # to the next line; in a column it takes the full width.
    width: str | None = None
    paginate: str | None = None
    debug: str | None = None
