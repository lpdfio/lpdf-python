# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ChartAttr:
    """
    A chart drawn from numbers, written like a table: series are its columns, each category
    a row and each value a cell, a value for each series in the series' order. A chart with
    one series needs no series. It takes its box in the flow as an image does, never splits
    across pages, and moves whole to the next page when it doesn't fit. The engine draws its
    axis, steps, gridlines, labels and legend by fixed rules: the value axis of bars and
    areas starts at zero, and a line's fits its values, from a round step under the lowest
    to one over the highest; the axis runs in round steps, each 1, 2 or 5 times a power of
    ten, written in full; a negative value takes the axis below zero, where a zero line is
    drawn; a label wider than its room wraps at spaces onto three lines at most, and what
    still doesn't fit ends in an ellipsis, so a chart always renders. A line or an area
    writes every 2nd, 3rd or 5th label where they don't all fit, and every point keeps its
    place. A missing value breaks a line, an area and a sparkline, and counts as zero in a
    stacked area. A sparkline draws no axis, labels or legend. A pie or a donut draws no
    axis either: a slice for each category, clockwise from the top, as wide as its share of
    the whole, in the largest circle the plot holds, and a legend at the right that lists
    each slice's label, color and share; a donut has a hole, with a text of the author's in
    it, and a negative value, or values that add up to zero, are refused. A chart is a leaf,
    with no padding, background or border: a column around it gives them, and a text above
    it is its title.
    """

    # The kind of chart. bar draws a bar for each value, side by side within a category, or
    # stacked with stacked="true". line draws a line through the values of each series, on an
    # axis that fits them. area draws a line filled down to zero, or with stacked="true" each
    # series filled down to the one under it. pie draws a slice for each category, as wide as
    # its share of the whole, with no axis. donut is a pie with a hole, which hole sizes and
    # hole-text writes in. sparkline draws one small line through the whole box, with no axis,
    # labels or legend, for a table cell.
    type: str
    # Height of the whole chart, a length or a name from the height row of the tokens. The axis,
    # the labels and the legend take room inside it and the width, and the plot gets the rest.
    # The width is fill unless it is set.
    height: str
    # Which way the bars run. vertical, the default, puts the categories along the bottom and
    # the value axis on the left; horizontal lists the categories down the left side, which
    # suits long labels, with the value axis along the bottom. Bars only: refused on any other
    # kind.
    direction: str | None = None
    # Stacks the bars of a category on each other, in the order of the series, or the areas of
    # the series, each filled down to the one under it, so the axis runs to the largest total. A
    # stacked value can't be negative, and a missing one counts as zero. Default false: side by
    # side, or areas filled down to zero. Bars and areas only: refused on any other kind.
    stacked: bool | None = None
    # Width of the element. A length fixes it. fill, in a row, takes the width its line leaves
    # after the other children, shared equally if several on the line use fill, and never moves
    # to the next line; in a column it takes the full width.
    width: str | None = None
    # Written before every number of the chart, the steps and the value labels: $ writes
    # $41,200.
    prefix: str | None = None
    # Written after every number of the chart: % writes 12%, and " ms" writes 12 ms. With values
    # in thousands, suffix="k" writes $412k.
    suffix: str | None = None
    # The decimals of the value labels, 0 to 6, and of the shares in the legend of a pie or a
    # donut, which are whole percents unless it says otherwise. Left out, a value is written
    # with the decimals it has. The steps of the axis take the decimals their size needs.
    decimals: int | None = None
    # A number the value axis reaches down to at least, which takes it below zero: min="-50". It
    # only widens the axis: a value below it still fits. On a line, whose axis fits its values,
    # min="0" brings the axis down to zero. A sparkline reaches it too, though it draws no axis.
    min: float | None = None
    # A number the value axis reaches at least: max="100" for percentages, or the same max on
    # charts meant to be compared side by side, such as the sparklines of a table. It only
    # widens the axis: a value above it still fits.
    max: float | None = None
    # The character between the groups of three digits of a number, or empty for none. Default
    # ,: with decimal-mark="," and thousands-mark=".", 1234.5 is written 1.234,5; with a space,
    # 1 234,5.
    thousands_mark: str | None = None
    # The character before the decimals of a number. Default ., and it can't be the
    # thousands-mark.
    decimal_mark: str | None = None
    # The space between the plot and the axis labels, and between them and the legend. Default
    # s, from the space row of the tokens.
    gap: str | None = None
    # The space between the bars of one category, side by side. Default a tenth of a bar.
    bar_gap: str | None = None
    # The space between categories. Default a quarter of the room of a category. The bars take
    # the room the two gaps leave.
    category_gap: str | None = None
    # Where the legend goes, which lists each series with its label and its color, or each slice
    # of a pie or a donut with its label, its color and its share of the whole, 22%: bottom,
    # top, right, or none. Default bottom with two series or more, and none with one; right for
    # a pie or a donut.
    legend: str | None = None
    # Writes each value at the end of its bar or over its point. A point lower than the points
    # beside it has its value under it, where its line doesn't run. The total of a stack goes at
    # the end of the stack or over its top. Default false. A sparkline writes none.
    value_labels: bool | None = None
    # The width of every line of a line, an area or a sparkline chart, a length such as 2pt:
    # 1.5pt by default, and 1pt for a sparkline. 0 draws no line, so an area is its fill alone.
    # Every line takes the same width: which line is the current one and which the comparison is
    # told by the series' color.
    stroke_width: str | None = None
    # The hole of a donut as a share of its size, from 0.1 to 0.9: 0.8 is a thin ring and 0.5 a
    # thick one. Default 0.6. Donuts only: refused on any other kind.
    hole: float | None = None
    # A text in the middle of a donut's hole, as it should read: a total, $11,100, or a share,
    # 72%. The engine adds nothing up. Too wide for the hole, it wraps at spaces, and what still
    # doesn't fit ends in an ellipsis. Donuts only: refused on any other kind.
    hole_text: str | None = None
    font: str | None = None
    font_size: str | None = None
    # The color of the chart's text, its labels, steps and legend, and of its zero line. Default
    # the color of the text around it. A sparkline, which has no text, draws its line in it, and
    # without it in the first color of the palette.
    color: str | None = None
    # What the chart shows, which a screen reader reads in a tagged document, one with pdfua or
    # a pdfa of level a: "Revenue per month, highest in March". alt="" marks it as decoration. A
    # PDF/UA document needs it on every chart of the layout; at PDF/A level a without pdfua, a
    # chart without it is decoration. A document that is not tagged ignores it.
    alt: str | None = None
