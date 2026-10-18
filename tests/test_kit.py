import pytest

from lpdf import (
    L, NoAttr,
    ColumnAttr, GridAttr, LinkAttr, TextAttr, SpanAttr,
    DividerAttr, SectionAttr, DocumentAttr, DocumentMeta, DocumentTokens, LayoutAttr,
    LayerAttr, RectAttr,
)


# ── Layout container nodes ────────────────────────────────────────────────────

def test_column_empty():
    node = L.column()
    d = node.to_dict()
    assert d == {"type": "column", "attrs": {}, "nodes": []}


def test_column_with_options():
    node = L.column(ColumnAttr(gap="10pt", padding="5pt"))
    d = node.to_dict()
    assert d["attrs"] == {"gap": "10pt", "padding": "5pt"}


def test_snake_to_kebab_conversion():
    node = L.text(TextAttr(font_size="12pt", align="center"), ["hello"])
    d = node.to_dict()
    assert d["attrs"] == {"font-size": "12pt", "align": "center"}


def test_grid_col_width():
    node = L.grid(GridAttr(cols="3", col_width="100pt"))
    d = node.to_dict()
    assert d["attrs"] == {"cols": "3", "col-width": "100pt"}


def test_container_types():
    for method, name in [
        ("column", "column"), ("row", "row"), ("grid", "grid"), ("frame", "frame"),
    ]:
        d = getattr(L, method)().to_dict()
        assert d["type"] == name
    assert L.link(LinkAttr(href="https://lpdf.io")).to_dict()["type"] == "link"


def test_text_with_string_children():
    node = L.text(NoAttr, ["Hello", " world"])
    d = node.to_dict()
    assert d == {"type": "text", "attrs": {}, "nodes": ["Hello", " world"]}


def test_text_with_span_children():
    s = L.span(SpanAttr(bold="true"), ["bold text"])
    node = L.text(NoAttr, ["Normal ", s])
    d = node.to_dict()
    assert d["nodes"][0] == "Normal "
    assert d["nodes"][1] == {"type": "span", "attrs": {"bold": "true"}, "nodes": ["bold text"]}


def test_divider():
    node = L.divider(DividerAttr(color="red", thickness="2pt"))
    d = node.to_dict()
    assert d == {"type": "divider", "attrs": {"color": "red", "thickness": "2pt"}}


# ── L.section / layout / canvas wrappers ────────────────────────────────────

def test_section():
    layout = L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])
    section = L.section(SectionAttr(size="a4", background="#ffffff"), [layout])
    d = section.to_dict()
    assert d["type"] == "section"
    assert d["attrs"] == {"size": "a4", "background": "#ffffff"}
    assert len(d["nodes"]) == 1


def test_layout_wrapper():
    layout = L.layout(NoAttr, [L.text(NoAttr, ["hi"])])
    d = layout.to_dict()
    assert d["type"] == "layout"
    assert d["attrs"] == {}
    assert "nodes" in d


def test_layout_margin():
    layout = L.layout(LayoutAttr(margin="20pt 30pt"), [])
    assert layout.to_dict()["attrs"] == {"margin": "20pt 30pt"}


def test_layers_go_directly_in_a_section_before_and_after_its_layout():
    section = L.section(NoAttr, [
        L.layer(LayerAttr(page="first"), [L.rect(RectAttr(width="10pt", height="10pt"))]),
        L.layout(NoAttr, [L.text(NoAttr, ["hi"])]),
        L.layer(LayerAttr(page="last"), [L.rect(RectAttr(width="20pt", height="20pt"))]),
    ])
    d = section.to_dict()
    assert [n["type"] for n in d["nodes"]] == ["layer", "layout", "layer"]
    assert d["nodes"][0]["attrs"] == {"page": "first"}
    assert d["nodes"][2]["attrs"] == {"page": "last"}


def test_there_is_no_canvas():
    assert not hasattr(L, "canvas")


def test_document_includes_version():
    doc = L.document()
    d = doc.to_dict()
    assert d["version"] == 1
    assert d["type"] == "document"


def test_document_with_meta_and_tokens():
    doc = L.document(
        DocumentAttr(
            size="a4",
            meta=DocumentMeta(title="Test", author="Me"),
            tokens=DocumentTokens(colors={"primary": "#000"}),
        ),
    )
    d = doc.to_dict()
    assert d["attrs"]["size"] == "a4"
    assert d["attrs"]["meta"] == {"title": "Test", "author": "Me"}
    assert d["attrs"]["tokens"] == {"colors": {"primary": "#000"}}


def test_a_line_height_row_is_a_token_row_under_its_schema_name():
    row = {"xs": "1", "m": "1.2", "xxl": "2"}
    d = L.document(DocumentAttr(tokens=DocumentTokens(line_height=row))).to_dict()
    assert d["attrs"]["tokens"] == {"line-height": row}


def test_a_text_line_height_is_a_token_or_a_factor_under_its_schema_name():
    assert L.text(TextAttr(line_height="l"), ["A token"]).to_dict()["attrs"] == {"line-height": "l"}
    assert L.text(TextAttr(line_height="1.5"), ["A factor"]).to_dict()["attrs"] == {"line-height": "1.5"}


def test_none_options_skipped():
    node = L.text(TextAttr(font="Arial"), ["hi"])
    d = node.to_dict()
    assert d["attrs"] == {"font": "Arial"}
    assert "font-size" not in d["attrs"]


def test_section_uses_section_type_not_page():
    """Regression: serialised type must be 'section', not 'page'."""
    section = L.section()
    assert section.to_dict()["type"] == "section"


def test_nodes_key_not_children():
    """Regression: serialised key must be 'nodes', not 'children'."""
    node = L.column(nodes=[L.text(NoAttr, ["x"])])
    d = node.to_dict()
    assert "nodes" in d
    assert "children" not in d
