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
    ``pdfua`` writes the PDF as PDF/UA-1, a tagged PDF a screen reader can read: ``"1"``. It combines with ``pdfa``.
    The render needs ``created_on``, the meta a ``title`` and a ``lang``, every image and barcode of the layout an
    ``alt``, and every text a font of the assets. What PDF/UA cannot hold is an error that says what to change.
    ``pdfx`` writes the PDF as PDF/X-4, for a commercial printer: ``"4"``. It needs ``profile``, and combines with
    ``pdfua``. Every page gets a TrimBox and a BleedBox, RGB is tied to sRGB, and links print as text, as PDF/X allows
    nothing clickable. The render needs ``created_on``, the meta a ``title``, and every text a font of the assets. What
    PDF/X cannot hold is an error that says what to change: a profile that is not a printer profile, a built-in font,
    a form field, a CMYK color with a profile that is not a CMYK one, ``encrypt``, ``pdfa``, attachments.
    ``profile`` is the profile of the assets that a PDF/X file is made for: the ICC profile of the printing press. It
    needs ``pdfx``.
    """

    encrypt: str | None = None
    allow: str | None = None
    pdfa: str | None = None
    pdfua: str | None = None
    pdfx: str | None = None
    profile: str | None = None

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in dc_fields(self) if getattr(self, f.name) is not None}
