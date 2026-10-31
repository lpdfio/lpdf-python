from __future__ import annotations

from dataclasses import fields
from typing import Any


def _snake_to_kebab(name: str) -> str:
    return name.replace("_", "-")


def options_to_attrs(options: Any, *, skip: tuple[str, ...] = ()) -> dict[str, Any]:
    """Convert a frozen dataclass of options into a flat dict of kebab-case attrs.

    Each value is kept as it is given: ``bold=True`` and ``cols=3`` stay a boolean and a number in the tree.
    Python doesn't check the types of a dataclass, so a value of the wrong type, such as ``cols="3"``, reaches the
    engine as it is, and the engine refuses it when it renders. Fields that are ``None`` are left out.
    """
    if options is None:
        return {}
    attrs: dict[str, Any] = {}
    for f in fields(options):
        if f.name in skip:
            continue
        value = getattr(options, f.name)
        if value is not None:
            attrs[_snake_to_kebab(f.name)] = value
    return attrs


def node_to_dict(node: Any) -> Any:
    """Convert a node (str or object with to_dict()) to a serialisable value."""
    if isinstance(node, str):
        return node
    return node.to_dict()
