from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MergeOptions:
    """
    What a ``PdfEngine.merge`` does beyond its defaults. Each is off by default.
    """

    # Merge a file that is signed. A signature covers the bytes of its own file, so it is lost in the merged file, and
    # what it looked like still prints. Without it, a signed file is an error that names the file.
    allow_signed: bool = False
    # Merge a file whose owner password restricts printing or copying, which opens without a password. Without it, such
    # a file is an error that names the file.
    allow_restricted: bool = False
    # Add a blank side after a document that has an odd number of pages, the size of its last page, so that each
    # document starts on a front side when the result is printed on both sides of the sheet. None is added after the
    # last document.
    double_sided: bool = False
