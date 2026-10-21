from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields

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
    line_height: dict[str, str] | None = None
    gradients: dict[str, Gradient] | None = None
    # Names for the slots of the scale: {"caption": "xs"} lets font_size="caption" mean the text size xs.
    aliases: dict[str, str] | None = None
    # The heights that height="m" names, from xs to xxl.
    height: dict[str, str] | None = None

    def to_dict(self) -> dict:
        _rename = {"text_size": "text-size", "line_height": "line-height"}
        return {
            _rename.get(f.name, f.name): getattr(self, f.name)
            for f in dc_fields(self)
            if getattr(self, f.name) is not None
        }
