from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields


@dataclass(frozen=True)
class DocumentOutput:
    """How the PDF file is written, as the ``output`` element of the XML is: whether it is encrypted, and what a
    reader may do with it, and the standard it meets. The passwords are not here: they come with the render call, on
    ``RenderOptions``.

    ``encrypt`` is the cipher, ``"aes-256"`` or ``"rc4-128"`` (``Cipher``); without it the PDF is not encrypted.
    ``allow`` is what a reader may do without the owner password, separated by spaces (``Permission``): ``all``, or
    any of ``print``, ``modify``, ``copy``, ``annotate``, ``fill-forms``, ``accessibility``, ``assemble``. A
    permission comes only from naming it: without ``allow``, or with ``""``, nothing is allowed, and ``all`` allows
    everything. It needs ``encrypt``.
    ``pdfa`` writes the PDF as PDF/A, the standard for files kept for the long term: ``"2b"``, or ``"2u"`` when its
    text must also be searchable. The render needs ``created_on``, and every text a font of the assets. What PDF/A
    cannot hold is an error that says what to change: a built-in font, a CMYK color, a form field, a barcode's
    digits, ``encrypt``.
    """

    encrypt: str | None = None
    allow: str | None = None
    pdfa: str | None = None

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in dc_fields(self) if getattr(self, f.name) is not None}
