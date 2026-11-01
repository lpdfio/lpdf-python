# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MarkdownQuoteAttr:
    """
    A block quote, written > in Markdown: a bar beside its content. font, font-size, color,
    line-height and align set the words; padding, background, border and radius the box
    around the bar and the words; bar-color and bar-width the bar, a strip along the left of
    the box: bar-width is a length or a name from the space row of the tokens.
    """

    font: str | None = None
    font_size: str | None = None
    bold: bool | None = None
    color: str | None = None
    align: str | None = None
    line_height: str | float | None = None
    padding: str | None = None
    background: str | None = None
    border: str | None = None
    radius: str | None = None
    bar_color: str | None = None
    bar_width: str | None = None
