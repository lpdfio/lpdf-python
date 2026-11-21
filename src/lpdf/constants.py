# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum

__all__ = [
    "PageSize",
    "Orientation",
    "SectionType",
    "ColumnFill",
    "Grow",
    "FootnoteCounter",
    "Cipher",
    "PdfALevel",
    "PdfUaPart",
    "PdfXVersion",
    "TextRole",
    "Permission",
    "FileRelationship",
    "GradientType",
    "RulingOrigin",
    "BoxAlign",
    "Align",
    "BoxJustify",
    "CaptureMode",
    "Paginate",
    "RowKeep",
    "Ocg",
    "ListType",
    "ListFormat",
    "ListBullet",
    "TextAlign",
    "Anchor",
    "PageScope",
    "LineCap",
    "FillRule",
    "Pin",
    "BarcodeType",
    "QrEcLevel",
    "Pdf417EcLevel",
    "DividerDirection",
    "ShapeType",
    "CellVAlign",
    "FieldType",
    "BuiltinFont",
    "StampScale",
]


class PageSize(StrEnum):
    """The named values of the `size` attribute of a document or a section. A width and a height, such as 100pt 200pt, is a string."""

    A4 = "a4"
    A3 = "a3"
    A5 = "a5"
    LETTER = "letter"
    LEGAL = "legal"


class Orientation(StrEnum):
    """The values of the `orientation` attribute of a document or a section."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class SectionType(StrEnum):
    """The values of the `type` attribute of a section."""

    TOC = "toc"


class ColumnFill(StrEnum):
    """How the columns of a section's last page fill: in order, as on every other page, or levelled."""

    AUTO = "auto"
    BALANCE = "balance"


class Grow(StrEnum):
    """The sizes a section's page grows in to fit its content: width, height, or both."""

    WIDTH = "width"
    HEIGHT = "height"
    WIDTH_HEIGHT = "width height"


class FootnoteCounter(StrEnum):
    """Where the numbers of the footnotes start over: on every page, in every section, or never."""

    PAGE = "page"
    SECTION = "section"
    DOCUMENT = "document"


class Cipher(StrEnum):
    """The cipher a PDF is encrypted with: AES-256, or RC4-128 for readers that cannot open AES-256. PDF 2.0 deprecates RC4-128."""

    AES_256 = "aes-256"
    RC4_128 = "rc4-128"


class PdfALevel(StrEnum):
    """A level of PDF/A, the ISO 19005 standard for files kept for the long term: 2b keeps the look of every page, 2u adds that all text maps to Unicode, so it can be searched and copied, and 2a adds to 2u the tagged structure a screen reader reads. 3a, 3b and 3u are the same levels in part 3, which also carries files of any kind, as a Factur-X or ZUGFeRD e-invoice carries its XML."""

    LEVEL_2A = "2a"
    LEVEL_2B = "2b"
    LEVEL_2U = "2u"
    LEVEL_3A = "3a"
    LEVEL_3B = "3b"
    LEVEL_3U = "3u"


class PdfUaPart(StrEnum):
    """A part of PDF/UA, the ISO 14289 standard for PDFs that a screen reader can read: 1, the part the accessibility laws and the validators point at."""

    PART_1 = "1"


class PdfXVersion(StrEnum):
    """A version of PDF/X, the ISO 15930 standard for files sent to a commercial printer: 4, which keeps RGB colors, images and transparency, tied to color profiles."""

    VERSION_4 = "4"


class TextRole(StrEnum):
    """What a text is to a reader, beyond a paragraph: a heading of level 1 to 6."""

    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"


class Permission(StrEnum):
    """What a reader of an encrypted PDF may do without the owner password: all of what follows, or print (at full quality), modify, copy, annotate, fill in forms, extract text for accessibility tools, and assemble (insert, delete and rotate pages)."""

    ALL = "all"
    PRINT = "print"
    MODIFY = "modify"
    COPY = "copy"
    ANNOTATE = "annotate"
    FILL_FORMS = "fill-forms"
    ACCESSIBILITY = "accessibility"
    ASSEMBLE = "assemble"


class FileRelationship(StrEnum):
    """How a file the PDF carries relates to the document: source, the file the document was made from; data, the data its pages show, such as the XML of an e-invoice; alternative, the same content in another form; supplement, more than the pages show; or unspecified."""

    SOURCE = "source"
    DATA = "data"
    ALTERNATIVE = "alternative"
    SUPPLEMENT = "supplement"
    UNSPECIFIED = "unspecified"


class GradientType(StrEnum):
    """The values of the `type` attribute of a gradient."""

    LINEAR = "linear"
    RADIAL = "radial"


class RulingOrigin(StrEnum):
    """The values of the `origin` attribute of a ruling: the space its lines fill."""

    PAGE = "page"
    MARGIN = "margin"


class BoxAlign(StrEnum):
    """The values of the `align` attribute of a column and a row: how the children sit across the box."""

    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"


class Align(StrEnum):
    """The values of the `align` attribute of a td: how its content sits across the cell."""

    START = "start"
    CENTER = "center"
    END = "end"


class BoxJustify(StrEnum):
    """The values of the `justify` attribute of a column and a row: how the children are spread along the box."""

    START = "start"
    CENTER = "center"
    END = "end"
    BETWEEN = "between"


class CaptureMode(StrEnum):
    """The values of the `capture-mode` attribute of a text: which of the captured texts it shows."""

    FIRST = "first"
    LAST = "last"


class Paginate(StrEnum):
    """The values of the `paginate` attribute: where a box falls in the page flow."""

    NO = "no"
    BREAK_BEFORE = "break-before"
    BREAK_AFTER = "break-after"
    KEEP_NEXT = "keep-next"


class RowKeep(StrEnum):
    """The value of the `keep` attribute of a tr."""

    WITH_NEXT = "with-next"


class Ocg(StrEnum):
    """The values of the `ocg` attribute of an element, a layer or a ruling: an optional content group, a PDF layer that shows on screen only or in print only."""

    PRINT = "print"
    SCREEN = "screen"


class ListType(StrEnum):
    """The values of the `type` attribute of a list: what marks its items."""

    BULLET = "bullet"
    NUMBER = "number"


class ListFormat(StrEnum):
    """The values of the `format` attribute of a list and the `page-format` attribute of a section: how numbers are written."""

    DECIMAL = "decimal"
    LOWER_ALPHA = "lower-alpha"
    UPPER_ALPHA = "upper-alpha"
    LOWER_ROMAN = "lower-roman"
    UPPER_ROMAN = "upper-roman"


class ListBullet(StrEnum):
    """The values of the `bullet` attribute of a list and a li: the shape that marks the items of a bullet list."""

    DISC = "disc"
    CIRCLE = "circle"
    SQUARE = "square"
    DASH = "dash"


class TextAlign(StrEnum):
    """The values of the `align` attribute of a text, a text-at and the markdown rules: how the lines of a text align."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class Anchor(StrEnum):
    """The values of the `anchor` attribute of a layer shape, a text-at, an img-at and a barcode-at: the nine reference points of a page and of a box."""

    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    TOP_RIGHT = "top-right"
    CENTER_LEFT = "center-left"
    CENTER = "center"
    CENTER_RIGHT = "center-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    BOTTOM_RIGHT = "bottom-right"


class PageScope(StrEnum):
    """The named values of the `page` attribute of a layer or a region. A range such as 2-4 or 1,3-5 is a string."""

    EACH = "each"
    FIRST = "first"
    LAST = "last"
    ODD = "odd"
    EVEN = "even"


class LineCap(StrEnum):
    """The values of the `line-cap` attribute of a line and a path: how a stroke ends."""

    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class FillRule(StrEnum):
    """The values of the `fill-rule` attribute of a path."""

    NONZERO = "nonzero"
    EVENODD = "evenodd"


class Pin(StrEnum):
    """The values of the `pin` attribute of a region."""

    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    INSET = "inset"


class BarcodeType(StrEnum):
    """The values of the `type` attribute of a barcode: the kind of code."""

    QR = "qr"
    CODE128 = "code128"
    EAN13 = "ean13"
    CODE39 = "code39"
    EAN8 = "ean8"
    UPCA = "upca"
    DATAMATRIX = "datamatrix"
    PDF417 = "pdf417"
    GS1_128 = "gs1-128"
    GS1_DATAMATRIX = "gs1-datamatrix"


class QrEcLevel(StrEnum):
    """The values of the `ec` attribute of a qr: its error correction, from 7% to 30% of the code."""

    L = "L"
    M = "M"
    Q = "Q"
    H = "H"


class Pdf417EcLevel(StrEnum):
    """The values of the `ec` attribute of a pdf417: its error correction level, from 0 to 8."""

    LEVEL_0 = "0"
    LEVEL_1 = "1"
    LEVEL_2 = "2"
    LEVEL_3 = "3"
    LEVEL_4 = "4"
    LEVEL_5 = "5"
    LEVEL_6 = "6"
    LEVEL_7 = "7"
    LEVEL_8 = "8"


class DividerDirection(StrEnum):
    """The values of the `direction` attribute of a divider."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ShapeType(StrEnum):
    """The values of the `type` attribute of a shape."""

    RECT = "rect"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"


class CellVAlign(StrEnum):
    """The values of the `valign` attribute of a td: how its content sits down the cell."""

    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


class FieldType(StrEnum):
    """The values of the `type` attribute of a field."""

    TEXT = "text"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"
    RADIO = "radio"
    BUTTON = "button"


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


class StampScale(StrEnum):
    """The values of the `scale` option of a stamp: how its image is sized in its box, keeping its proportions."""

    FIT = "fit"
    FILL = "fill"
