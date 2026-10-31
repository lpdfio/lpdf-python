# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class FileRelationship(StrEnum):
    """The values of the `relationship` attribute of a file the PDF carries: how it relates to the document."""

    SOURCE = "source"
    DATA = "data"
    ALTERNATIVE = "alternative"
    SUPPLEMENT = "supplement"
    UNSPECIFIED = "unspecified"
