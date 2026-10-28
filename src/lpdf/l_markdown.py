from __future__ import annotations

from .markdown.markdown_aattr import MarkdownAAttr
from .markdown.markdown_code_attr import MarkdownCodeAttr
from .markdown.markdown_content_node import MarkdownContentNode
from .markdown.markdown_del_attr import MarkdownDelAttr
from .markdown.markdown_em_attr import MarkdownEmAttr
from .markdown.markdown_h1_attr import MarkdownH1Attr
from .markdown.markdown_h2_attr import MarkdownH2Attr
from .markdown.markdown_h3_attr import MarkdownH3Attr
from .markdown.markdown_h4_attr import MarkdownH4Attr
from .markdown.markdown_h5_attr import MarkdownH5Attr
from .markdown.markdown_h6_attr import MarkdownH6Attr
from .markdown.markdown_li_attr import MarkdownLiAttr
from .markdown.markdown_pattr import MarkdownPAttr
from .markdown.markdown_quote_attr import MarkdownQuoteAttr
from .markdown.markdown_rule_node import MarkdownRuleNode
from .markdown.markdown_strong_attr import MarkdownStrongAttr
from .markdown.markdown_styles_attr import MarkdownStylesAttr
from .markdown.markdown_styles_node import MarkdownStylesNode
from .markdown.markdown_table_attr import MarkdownTableAttr
from .markdown.markdown_td_attr import MarkdownTdAttr
from .markdown.markdown_th_attr import MarkdownThAttr
from .shared.attrs_helper import options_to_attrs


class LMarkdown:
    """The parts of a markdown: its styles, its content and the rules of its styles. The markdown itself is
    ``L.markdown``.

    ::

        L.markdown(MarkdownAttr(margin="54pt", gap="m"), [
            LMarkdown.styles(NoAttr, [LMarkdown.h1(MarkdownH1Attr(color="muted"))]),
            LMarkdown.content(NoAttr, [body]),
        ])

    ``del`` is a keyword in Python, so the rule of struck-through text is ``LMarkdown.del_``.
    """

    @staticmethod
    def styles(attrs: MarkdownStylesAttr | None = None, nodes: list[MarkdownRuleNode] | None = None) -> MarkdownStylesNode:
        """Build the rules that say how the parts of a markdown look. A rule is named after the Markdown it styles
        and takes the attributes of the element it becomes. A rule here overrides the same rule of the file that
        ``src`` names, which overrides the defaults."""
        return MarkdownStylesNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def content(attrs: None = None, nodes: list[str] | None = None) -> MarkdownContentNode:
        """Build the Markdown, as strings that make one text. The common indent of its lines is removed, so that
        indenting the code does not make a code block of it. It has no attributes: pass ``NoAttr``."""
        for index, child in enumerate(nodes or []):
            if not isinstance(child, str):
                raise TypeError(f"content() child at index {index} must be a string, got {type(child).__name__}")
        return MarkdownContentNode(list(nodes or []))

    @staticmethod
    def h1(attrs: MarkdownH1Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 1."""
        return MarkdownRuleNode("h1", options_to_attrs(attrs))

    @staticmethod
    def h2(attrs: MarkdownH2Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 2."""
        return MarkdownRuleNode("h2", options_to_attrs(attrs))

    @staticmethod
    def h3(attrs: MarkdownH3Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 3."""
        return MarkdownRuleNode("h3", options_to_attrs(attrs))

    @staticmethod
    def h4(attrs: MarkdownH4Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 4."""
        return MarkdownRuleNode("h4", options_to_attrs(attrs))

    @staticmethod
    def h5(attrs: MarkdownH5Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 5."""
        return MarkdownRuleNode("h5", options_to_attrs(attrs))

    @staticmethod
    def h6(attrs: MarkdownH6Attr | None = None) -> MarkdownRuleNode:
        """Build the rule of a heading of level 6."""
        return MarkdownRuleNode("h6", options_to_attrs(attrs))

    @staticmethod
    def p(attrs: MarkdownPAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a paragraph, and of the words of a list item, a quote and a footnote."""
        return MarkdownRuleNode("p", options_to_attrs(attrs))

    @staticmethod
    def code(attrs: MarkdownCodeAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of code: the box of a block, and the run of inline code."""
        return MarkdownRuleNode("code", options_to_attrs(attrs))

    @staticmethod
    def quote(attrs: MarkdownQuoteAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a block quote."""
        return MarkdownRuleNode("quote", options_to_attrs(attrs))

    @staticmethod
    def li(attrs: MarkdownLiAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of an item of a bullet or a numbered list."""
        return MarkdownRuleNode("li", options_to_attrs(attrs))

    @staticmethod
    def a(attrs: MarkdownAAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a link."""
        return MarkdownRuleNode("a", options_to_attrs(attrs))

    @staticmethod
    def strong(attrs: MarkdownStrongAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of strong text."""
        return MarkdownRuleNode("strong", options_to_attrs(attrs))

    @staticmethod
    def em(attrs: MarkdownEmAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of emphasis."""
        return MarkdownRuleNode("em", options_to_attrs(attrs))

    @staticmethod
    def del_(attrs: MarkdownDelAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of struck-through text."""
        return MarkdownRuleNode("del", options_to_attrs(attrs))

    @staticmethod
    def table(attrs: MarkdownTableAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a table."""
        return MarkdownRuleNode("table", options_to_attrs(attrs))

    @staticmethod
    def th(attrs: MarkdownThAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a cell of a table's header row."""
        return MarkdownRuleNode("th", options_to_attrs(attrs))

    @staticmethod
    def td(attrs: MarkdownTdAttr | None = None) -> MarkdownRuleNode:
        """Build the rule of a cell of a table's other rows."""
        return MarkdownRuleNode("td", options_to_attrs(attrs))
