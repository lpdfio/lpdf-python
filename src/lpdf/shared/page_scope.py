# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class PageScope(StrEnum):
    """The named values of the `page` attribute of a layer or a region. A range such as 2-4 or 1,3-5 is a string."""

    EACH = "each"
    FIRST = "first"
    LAST = "last"
    ODD = "odd"
    EVEN = "even"
