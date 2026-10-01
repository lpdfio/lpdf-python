from __future__ import annotations

from dataclasses import dataclass

from .document_assets import DocumentAssets
from .document_meta import DocumentMeta
from .document_tokens import DocumentTokens


@dataclass(frozen=True)
class DocumentAttr:
    size: str | None = None
    orientation: str | None = None
    margin: str | None = None
    background: str | None = None
    font: str | None = None
    debug: str | None = None
    assets: DocumentAssets | None = None
    tokens: DocumentTokens | None = None
    meta: DocumentMeta | None = None
