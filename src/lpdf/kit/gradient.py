from __future__ import annotations

from typing import TypedDict

from .gradient_stop import GradientStop

# A gradient of the tokens, which a background or a fill uses as ``gradient:name``. ``type`` (``linear`` or
# ``radial``) is required by the engine. Give ``from`` and ``to`` for two colors, or ``stops`` for more.
# ``angle`` is the direction of a linear gradient in degrees: 0 runs top to bottom and 90 left to right.
# The functional form, because ``from`` is a Python keyword.
Gradient = TypedDict(
    "Gradient",
    {
        "type": str,
        "from": str,
        "to": str,
        "angle": "int | float | str",
        "stops": "list[GradientStop]",
    },
    total=False,
)
