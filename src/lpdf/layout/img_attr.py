# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImgAttr:
    """Attributes of the `img` element."""

    name: str
    height: str | None = None
    width: str | None = None
    font: str | None = None
    font_size: str | None = None
    gap: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
    paginate: str | None = None
    debug: str | None = None
