# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BarcodeAttr:
    """Attributes of the `barcode` element."""

    type: str
    data: str
    size: str | None = None
    width: str | None = None
    height: str | None = None
    ec: str | None = None
    hrt: str | None = None
    color: str | None = None
    background: str | None = None
    debug: str | None = None
