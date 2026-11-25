from __future__ import annotations

import math
from decimal import Decimal

from .layout.chart_category_attr import ChartCategoryAttr
from .layout.chart_category_node import ChartCategoryNode
from .layout.chart_series_attr import ChartSeriesAttr
from .layout.chart_series_node import ChartSeriesNode
from .layout.chart_value_node import ChartValueNode
from .shared.attrs_helper import options_to_attrs


def plain_number(value: int | float | Decimal) -> str:
    """A number as the text of a chart's value: in full, with no exponent, which ``str(1e21)`` and ``str(1e-07)``
    write, and a whole float without its ``.0``, as the other SDKs write it. A ``Decimal`` keeps its decimals:
    ``Decimal("0.250")`` is ``0.250``, and ``Decimal("1E+3")`` is ``1000``.

    :raises ValueError: when the float or the Decimal is not finite.
    """
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError(f"a chart's value is a finite number, not {value}")
        return format(value.copy_abs() if value.is_zero() else value, "f")
    if not math.isfinite(value):
        raise ValueError(f"a chart's value is a finite number, not {value}")
    if value == 0:
        return "0"
    # repr gives the shortest digits that read back as the float, which Decimal writes out in full: 1e23 is
    # 100000000000000000000000, not the 99999999999999991611392 of its binary value.
    text = format(Decimal(repr(value)), "f")
    return text.removesuffix(".0") if value.is_integer() else text


class LChart:
    """The parts of a chart: its series, its categories and their values. The chart itself is ``L.chart``.

    ::

        L.chart(ChartAttr(type=ChartType.BAR, height="160pt", prefix="$"), [
            LChart.series(ChartSeriesAttr(label="Revenue")),
            LChart.category(ChartCategoryAttr(label="Q1"), [LChart.value(NoAttr, [120000])]),
        ])
    """

    @staticmethod
    def series(attrs: ChartSeriesAttr | None = None) -> ChartSeriesNode:
        """Build a series of a chart: its entry in the legend and the color of its bars, line or area."""
        return ChartSeriesNode(options_to_attrs(attrs))

    @staticmethod
    def category(
        attrs: ChartCategoryAttr | None = None, nodes: list[ChartValueNode] | None = None
    ) -> ChartCategoryNode:
        """Build a category of a chart: a value for each series, in their order, and its label."""
        return ChartCategoryNode(options_to_attrs(attrs), list(nodes or []))

    @staticmethod
    def value(attrs: None = None, nodes: list[int | float | Decimal | str] | None = None) -> ChartValueNode:
        """Build a value of a category: one number, written in full with no exponent and no locale, a ``Decimal``
        with its decimals, or a string that is a number, such as ``"0.250"``, taken as written so its label keeps its
        decimals. No value, ``[]``, draws no bar and breaks a line, an area or a sparkline; a stacked area counts it
        as zero. It has no attributes: pass ``NoAttr``.

        :raises TypeError: when a value is not an int, a float, a Decimal or a string.
        :raises ValueError: when a float or a Decimal is not finite.
        """
        texts: list[str] = []
        for index, child in enumerate(nodes or []):
            if isinstance(child, str):
                texts.append(child)
            elif isinstance(child, (int, float, Decimal)) and not isinstance(child, bool):
                texts.append(plain_number(child))
            else:
                raise TypeError(
                    f"value() child at index {index} must be an int, a float, a Decimal or a string, "
                    f"got {type(child).__name__}"
                )
        return ChartValueNode(texts)
