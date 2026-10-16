# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PathAttr:
    """Attributes of the `path` element in a layer."""

    d: str
    fill: str | None = None
    stroke: str | None = None
    fill_rule: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    line_cap: str | None = None
    opacity: str | None = None
