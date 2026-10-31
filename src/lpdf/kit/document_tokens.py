from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields

from ..shared.attrs_helper import assert_finite_in
from .gradient import Gradient


@dataclass(frozen=True)
class DocumentTokens:
    colors: dict[str, str] | None = None
    space: dict[str, str] | None = None
    grid: dict[str, str] | None = None
    border: dict[str, str] | None = None
    radius: dict[str, str] | None = None
    width: dict[str, str] | None = None
    text_size: dict[str, str] | None = None
    # The factors line_height names, each a number above 0: {"xs": 1, "m": 1.2} and so on.
    line_height: dict[str, float] | None = None
    gradients: dict[str, Gradient] | None = None
    # Names for the slots of the scale: {"caption": "xs"} lets font_size="caption" mean the text size xs.
    aliases: dict[str, str] | None = None
    # The heights that height="m" names, from xs to xxl.
    height: dict[str, str] | None = None

    def to_dict(self) -> dict:
        _rename = {"text_size": "text-size", "line_height": "line-height"}
        for f in dc_fields(self):
            # A factor of the line-height row and a gradient's angle are numbers, which JSON can't hold as NaN.
            assert_finite_in(f"tokens.{f.name}", getattr(self, f.name))
        return {
            _rename.get(f.name, f.name): getattr(self, f.name)
            for f in dc_fields(self)
            if getattr(self, f.name) is not None
        }
