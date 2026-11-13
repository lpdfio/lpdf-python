from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields

from ..shared.attrs_helper import assert_finite_in
from .gradient import Gradient
from .ruling import Ruling
from .spot import Spot


@dataclass(frozen=True, kw_only=True)
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
    # Lines a section draws on every page with ruling="name", by name: {"graph": {"origin": "margin", "lines":
    # [{"step": "5mm"}, {"step": "25mm"}]}}. Each set of lines is cut by a step or a count, in x, in y or both.
    rulings: dict[str, Ruling] | None = None
    # Spot colors, each an ink of its own printed from a plate of its own, by the name a color gives: {"brand": {"ink":
    # "PANTONE 1665 C", "value": "cmyk(0, 85, 100, 0)"}}. A color takes the name, or a tint after a space: "brand 30%".
    spots: dict[str, Spot] | None = None

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
