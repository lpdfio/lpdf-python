# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayerAttr:
    """
    Groups canvas shapes and sets what applies to all of them: which pages they appear on,
    opacity, transform and clip. Layers cannot be nested.
    """

    page: str | None = None
    opacity: str | None = None
    transform: str | None = None
    clip: str | None = None
