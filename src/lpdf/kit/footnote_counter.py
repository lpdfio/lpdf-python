# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class FootnoteCounter(StrEnum):
    """The values of the `footnote-counter` attribute of a document or a section."""

    PAGE = "page"
    SECTION = "section"
    DOCUMENT = "document"
