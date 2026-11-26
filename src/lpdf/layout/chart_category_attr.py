# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ChartCategoryAttr:
    """
    A category of a chart: a bar for each series, or a stack of them, or a point on each
    line, or a slice of a pie or a donut, with its label beside the axis, or in the legend
    of a pie or a donut. It holds a value for each series of the chart, after the data is
    bound. data-source repeats it for each item of a list. A chart holds 10,000 categories
    at most, counted after the data is bound.
    """

    # The category's label, under its bars or its point, or beside the bars with
    # direction="horizontal", or in the legend of a pie or a donut, before the slice's share.
    label: str | None = None
    # The color of the category's bar, in a bar chart of one series, where the series' color is
    # the default, or of its slice in a pie or a donut, where the default is the next color of
    # the palette.
    color: str | None = None
