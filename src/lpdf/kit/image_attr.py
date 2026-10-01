# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageAttr:
    """
    Declares an image that an img refers to by name. The SDK reads the file from src, or the
    image was loaded on the engine under ref or, with no ref, under its own name.
    """

    # The name that the name attribute of an img uses to pick this image: lowercase letters,
    # digits and -, starting with a letter.
    name: str
    # The key the image was loaded under on the engine, when that is not its name.
    ref: str | None = None
    # A path the SDK reads the image file from, when the image was not loaded on the engine.
    src: str | None = None
