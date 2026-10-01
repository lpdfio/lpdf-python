# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class Orientation(StrEnum):
    """The values of the `orientation` attribute of a document or a section."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
