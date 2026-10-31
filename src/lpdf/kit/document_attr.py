from __future__ import annotations

from dataclasses import dataclass

from .document_assets import DocumentAssets
from .document_meta import DocumentMeta
from .document_output import DocumentOutput
from .document_tokens import DocumentTokens
from .file_attr import FileAttr


@dataclass(frozen=True)
class DocumentAttr:
    """Document-level attributes applied as defaults to every section. ``attachments`` are the files the PDF carries
    inside it, as the ``attachments`` element of the XML is: a reader lists them in its attachments panel. Each file's
    bytes are read from its ``src``, or loaded with ``load_file`` under its ``ref`` or name."""

    size: str | None = None
    orientation: str | None = None
    background: str | None = None
    font: str | None = None
    debug: bool | None = None
    assets: DocumentAssets | None = None
    tokens: DocumentTokens | None = None
    meta: DocumentMeta | None = None
    footnote_counter: str | None = None
    output: DocumentOutput | None = None
    attachments: list[FileAttr] | None = None
