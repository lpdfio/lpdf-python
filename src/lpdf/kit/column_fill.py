# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class ColumnFill(StrEnum):
    """The values of the `column-fill` attribute of a section: how the columns of its last page fill."""

    AUTO = "auto"
    BALANCE = "balance"
