# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CodeSpanAttr:
    """
    A run of code inside a text: its words in Courier on a light tint, the tint drawn behind
    them. It is the inline twin of code, and like a span it is not broken inside: a run
    longer than a line runs on past it. White space in it collapses as in the text around
    it.
    """

    font: str | None = None
    color: str | None = None
    # The tint drawn behind the run. Default #f3f4f6.
    background: str | None = None
