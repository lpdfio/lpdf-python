# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldAttr:
    """Attributes of the `field` element."""

    type: str
    name: str
    value: str | None = None
    label: str | None = None
    options: str | None = None
    group: str | None = None
    checked: str | None = None
    required: str | None = None
    readonly: str | None = None
    max_len: str | None = None
    action_url: str | None = None
    width: str | None = None
    height: str | None = None
    background: str | None = None
    border: str | None = None
    debug: str | None = None
