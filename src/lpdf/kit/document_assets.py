from __future__ import annotations

from dataclasses import dataclass

from ..shared.attrs_helper import options_to_attrs
from .font_attr import FontAttr
from .image_attr import ImageAttr
from .profile_attr import ProfileAttr


@dataclass(frozen=True, kw_only=True)
class DocumentAssets:
    """The fonts, images and color profiles the document declares, as the ``assets`` element of the XML does.

    A font or image is picked by its ``name``: text sets ``font`` to a font's name, an ``img`` sets
    ``name`` to an image's, and the output's ``profile`` names a profile. ``profiles`` are ICC color profiles: the
    profile of the printing press a PDF/X document is made for, which the printer gives out. Each is read from its
    ``src``, or loaded with ``load_profile`` under its ``ref`` or name.
    """

    fonts: list[FontAttr] | None = None
    images: list[ImageAttr] | None = None
    profiles: list[ProfileAttr] | None = None

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        declared = {"fonts": self.fonts, "images": self.images, "profiles": self.profiles}
        return {
            kind: [options_to_attrs(item) for item in items]
            for kind, items in declared.items()
            if items
        }
