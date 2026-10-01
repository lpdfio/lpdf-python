# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class BuiltinFont(StrEnum):
    """The values of the `core` attribute of a font: the built-in PDF fonts, which need no file."""

    COURIER = "Courier"
    COURIER_BOLD = "Courier-Bold"
    COURIER_OBLIQUE = "Courier-Oblique"
    COURIER_BOLDOBLIQUE = "Courier-BoldOblique"
    HELVETICA = "Helvetica"
    HELVETICA_BOLD = "Helvetica-Bold"
    HELVETICA_OBLIQUE = "Helvetica-Oblique"
    HELVETICA_BOLDOBLIQUE = "Helvetica-BoldOblique"
    TIMES_ROMAN = "Times-Roman"
    TIMES_BOLD = "Times-Bold"
    TIMES_ITALIC = "Times-Italic"
    TIMES_BOLDITALIC = "Times-BoldItalic"
    SYMBOL = "Symbol"
    ZAPFDINGBATS = "ZapfDingbats"
