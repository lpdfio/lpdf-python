# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownCodeAttr:
    """
    Code: the box of a fenced or indented block, and the run of inline code, which takes the
    font, the color and the background. The language of a fence is ignored, since there is
    no highlighting by language.
    """

    font: str | None = None
    font_size: str | None = None
    color: str | None = None
    line_height: str | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
    tab_size: str | None = None
