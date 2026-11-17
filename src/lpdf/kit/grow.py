# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class Grow(StrEnum):
    """The values of the `grow` attribute of a section: the sizes its page grows in to fit its content."""

    WIDTH = "width"
    HEIGHT = "height"
    WIDTH_HEIGHT = "width height"
