from __future__ import annotations

import math
from dataclasses import fields
from typing import Any


def _snake_to_kebab(name: str) -> str:
    return name.replace("_", "-")


def options_to_attrs(options: Any, *, skip: tuple[str, ...] = ()) -> dict[str, Any]:
    """Convert a frozen dataclass of options into a flat dict of kebab-case attrs.

    Each value is kept as it is given: ``bold=True`` and ``cols=3`` stay a boolean and a number in the tree.
    Python doesn't check the types of a dataclass, so a value of the wrong type, such as ``cols="3"``, reaches the
    engine as it is, and the engine refuses it when it renders. A NaN or an infinity, which JSON can't hold, is
    refused here. Fields that are ``None`` are left out.

    Raises:
        ValueError: when a value is a float that isn't finite.
    """
    if options is None:
        return {}
    attrs: dict[str, Any] = {}
    for f in fields(options):
        if f.name in skip:
            continue
        value = getattr(options, f.name)
        if value is not None:
            name = _snake_to_kebab(f.name)
            assert_finite(name, value)
            attrs[name] = value
    return attrs


def assert_finite(name: str, value: Any) -> None:
    """Refuse a number a document can't hold, NaN or an infinity, naming where it is.

    JSON has no such number: ``json.dumps`` writes ``NaN``, which the engine can't read, and as text a string
    attribute would take it, such as a ``nan`` that pandas gives for a missing title.

    Raises:
        ValueError: when ``value`` is a float that isn't finite.
    """
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, not {value}")


def assert_finite_in(name: str, value: Any) -> None:
    """Refuse a number that isn't finite anywhere in ``value``, a dict or a list, named by its path from ``name``."""
    if isinstance(value, dict):
        for key, item in value.items():
            assert_finite_in(f"{name}.{key}", item)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_finite_in(f"{name}[{index}]", item)
    else:
        assert_finite(name, value)


def node_to_dict(node: Any) -> Any:
    """Convert a node (str or object with to_dict()) to a serialisable value."""
    if isinstance(node, str):
        return node
    return node.to_dict()
