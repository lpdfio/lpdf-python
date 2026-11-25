from __future__ import annotations

import math
from decimal import Decimal

from .layout.chart_category_attr import ChartCategoryAttr
from .layout.chart_category_node import ChartCategoryNode
from .layout.chart_series_attr import ChartSeriesAttr
from .layout.chart_series_node import ChartSeriesNode
from .layout.chart_value_node import ChartValueNode
from .shared.attrs_helper import options_to_attrs


def plain_number(value: int | float) -> str:
    """A number as the text of a chart's value: in full, with no exponent, which ``str(1e21)`` and ``str(1e-07)``
    write, and a whole float without its ``.0``, as the other SDKs write it.

    :raises ValueError: when the float is not finite.
    """
    if isinstance(value, int):
        return str(value)
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
        """Build a series of a chart: its entry in the legend and the color of its bars."""
        return ChartSeriesNode(options_to_attrs(attrs))

    @staticmethod
    def category(
        attrs: ChartCategoryAttr | None = None, nodes: list[ChartValueNode] | None = None
    ) -> ChartCategoryNode:
        """Build a category of a chart: a value for each series, in their order, and its label."""
        return ChartCategoryNode(options_to_attrs(attrs), list(nodes or []))

    @staticmethod
    def value(attrs: None = None, nodes: list[int | float | str] | None = None) -> ChartValueNode:
        """Build a value of a category: a number, written in full with no exponent and no locale, or a string that is
        one, such as ``"0.250"``, taken as written so its label keeps its decimals. No value, ``[]``, draws no bar. It
        has no attributes: pass ``NoAttr``.

        :raises TypeError: when a value is not an int, a float or a string.
        :raises ValueError: when a float is not finite.
        """
        texts: list[str] = []
        for index, child in enumerate(nodes or []):
            if isinstance(child, str):
                texts.append(child)
            elif isinstance(child, (int, float)) and not isinstance(child, bool):
                texts.append(plain_number(child))
            else:
                raise TypeError(
                    f"value() child at index {index} must be an int, a float or a string, "
                    f"got {type(child).__name__}"
                )
        return ChartValueNode(texts)
