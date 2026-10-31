from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields


@dataclass(frozen=True)
class DocumentOutput:
    """How the PDF file is written, as the ``output`` element of the XML is: whether it is encrypted, and what a
    reader may do with it. The passwords are not here: they come with the render call, on ``RenderOptions``.

    ``encrypt`` is the cipher, ``"aes-256"`` or ``"rc4-128"`` (``Cipher``); without it the PDF is not encrypted.
    ``allow`` is what a reader may do without the owner password, separated by spaces (``Permission``): ``print``,
    ``modify``, ``copy``, ``annotate``, ``fill-forms``, ``accessibility``, ``assemble``. Without it everything is
    allowed; ``""`` allows nothing. It needs ``encrypt``.
    """

    encrypt: str | None = None
    allow: str | None = None

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in dc_fields(self) if getattr(self, f.name) is not None}
