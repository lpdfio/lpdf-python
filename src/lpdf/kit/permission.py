# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class Permission(StrEnum):
    """The words of the `allow` attribute of the output, separated by spaces: what a reader of an encrypted PDF may do."""

    PRINT = "print"
    MODIFY = "modify"
    COPY = "copy"
    ANNOTATE = "annotate"
    FILL_FORMS = "fill-forms"
    ACCESSIBILITY = "accessibility"
    ASSEMBLE = "assemble"
