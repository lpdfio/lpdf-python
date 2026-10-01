from __future__ import annotations

from dataclasses import dataclass

from ..shared.attrs_helper import options_to_attrs
from .font_attr import FontAttr
from .image_attr import ImageAttr


@dataclass(frozen=True)
class DocumentAssets:
    """The fonts and images the document declares, as the ``assets`` element of the XML does.

    A font or image is picked by its ``name``: text sets ``font`` to a font's name, an ``img`` sets
    ``name`` to an image's.
    """

    fonts: list[FontAttr] | None = None
    images: list[ImageAttr] | None = None

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        declared = {"fonts": self.fonts, "images": self.images}
        return {
            kind: [options_to_attrs(item) for item in items]
            for kind, items in declared.items()
            if items
        }
