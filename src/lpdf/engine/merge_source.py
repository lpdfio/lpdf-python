from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MergeSource:
    """
    One file for ``PdfEngine.merge``: its name and the PDF's bytes.
    """

    # The file's name, such as contract-b.pdf. Every error about the file names it.
    name: str
    # The PDF's bytes.
    pdf: bytes
