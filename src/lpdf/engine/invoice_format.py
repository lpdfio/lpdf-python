from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class InvoiceFormat:
    """How the values of each type are written on the page, for ``LCrossIndustryInvoice``: each function takes the
    value in its normal form and the full name of its entry in the map, without the prefix or an item number
    (``seller.country``, ``lines.unit``), and returns the text to bind, a ``str``: any other return, None or a number
    too, is refused with a ``TypeError``. A type without a function is bound as the invoice has it.

    ``date`` gets a date as ``2026-10-31``, or ``2026-10`` and ``2026-W44`` for a month and a week. ``amount`` gets an
    amount as the invoice writes it, ``1250.10``. ``code`` gets a code as the invoice writes it, ``H87``, ``S``,
    ``381``: Lpdf carries no words for codes.
    """

    date: Callable[[str, str], str] | None = None
    amount: Callable[[str, str], str] | None = None
    code: Callable[[str, str], str] | None = None
