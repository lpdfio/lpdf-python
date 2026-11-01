# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class LineAttr:
    """Attributes of the `line` element in a layer."""

    x1: str
    y1: str
    x2: str
    y2: str
    stroke: str | None = None
    stroke_width: str | None = None
    stroke_dash: str | None = None
    line_cap: str | None = None
    # Puts the element, and everything in it, in an optional content group, which the viewer
    # shows or hides. print: printed, and not shown on screen. screen: shown on screen, and not
    # printed. The element keeps its room either way, so nothing moves. An element with a group
    # inside an element with another shows only where both show. Acrobat, Chrome and Firefox
    # switch the groups; Preview and Safari show everything, on screen and in print. Hidden
    # content is still in the file, where it can be selected and copied: it is not a way to keep
    # anything secret. A link in print content is drawn and does nothing, and a form field can't
    # be in print content: use a frame with a border for a box filled in by hand. With pdfa or
    # pdfua on the output, everything shows. With pdfx, the file is the print version: screen
    # content stays in it, off, and a reader can turn it on in a layers panel.
    ocg: str | None = None
