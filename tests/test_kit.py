import pytest

from lpdf import (
    Pdf, NoAttr,
    StackAttr, FlankAttr, GridAttr, TextAttr, SpanAttr,
    DividerAttr, SectionAttr, DocumentAttr, DocumentMeta, DocumentTokens,
)


# ── Layout container nodes ────────────────────────────────────────────────────

def test_stack_empty():
    node = Pdf.stack()
    d = node.to_dict()
    assert d == {"type": "stack", "attrs": {}, "nodes": []}


def test_stack_with_options():
    node = Pdf.stack(StackAttr(gap="10pt", padding="5pt"))
    d = node.to_dict()
    assert d["attrs"] == {"gap": "10pt", "padding": "5pt"}


def test_snake_to_kebab_conversion():
    node = Pdf.text(TextAttr(font_size="12pt", text_align="center"), ["hello"])
    d = node.to_dict()
    assert d["attrs"] == {"font-size": "12pt", "text-align": "center"}


def test_grid_col_width():
    node = Pdf.grid(GridAttr(cols="3", col_width="100pt"))
    d = node.to_dict()
    assert d["attrs"] == {"cols": "3", "col-width": "100pt"}


def test_container_types():
    for method, name in [
        ("stack", "stack"), ("flank", "flank"), ("split", "split"),
        ("cluster", "cluster"), ("grid", "grid"), ("frame", "frame"), ("link", "link"),
    ]:
        d = getattr(Pdf, method)().to_dict()
        assert d["type"] == name


def test_text_with_string_children():
    node = Pdf.text(NoAttr, ["Hello", " world"])
    d = node.to_dict()
    assert d == {"type": "text", "attrs": {}, "nodes": ["Hello", " world"]}


def test_text_with_span_children():
    s = Pdf.span(SpanAttr(bold="true"), ["bold text"])
    node = Pdf.text(NoAttr, ["Normal ", s])
    d = node.to_dict()
    assert d["nodes"][0] == "Normal "
    assert d["nodes"][1] == {"type": "span", "attrs": {"bold": "true"}, "nodes": ["bold text"]}


def test_divider():
    node = Pdf.divider(DividerAttr(color="red", thickness="2pt"))
    d = node.to_dict()
    assert d == {"type": "divider", "attrs": {"color": "red", "thickness": "2pt"}}


# ── Pdf.section / layout / canvas wrappers ────────────────────────────────────

def test_section():
    layout = Pdf.layout(NoAttr, [Pdf.text(NoAttr, ["Hello"])])
    section = Pdf.section(SectionAttr(size="a4", margin="28pt"), [layout])
    d = section.to_dict()
    assert d["type"] == "section"
    assert d["attrs"] == {"size": "a4", "margin": "28pt"}
    assert len(d["nodes"]) == 1


def test_layout_wrapper():
    layout = Pdf.layout(NoAttr, [Pdf.text(NoAttr, ["hi"])])
    d = layout.to_dict()
    assert d["type"] == "layout"
    assert "nodes" in d


def test_canvas_wrapper():
    canvas = Pdf.canvas(NoAttr)
    d = canvas.to_dict()
    assert d["type"] == "canvas"
    assert d["nodes"] == []


def test_document_includes_version():
    doc = Pdf.document()
    d = doc.to_dict()
    assert d["version"] == 1
    assert d["type"] == "document"


def test_document_with_meta_and_tokens():
    doc = Pdf.document(
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


def test_none_options_skipped():
    node = Pdf.text(TextAttr(font="Arial"), ["hi"])
    d = node.to_dict()
    assert d["attrs"] == {"font": "Arial"}
    assert "font-size" not in d["attrs"]


def test_section_uses_section_type_not_page():
    """Regression: serialised type must be 'section', not 'page'."""
    section = Pdf.section()
    assert section.to_dict()["type"] == "section"


def test_nodes_key_not_children():
    """Regression: serialised key must be 'nodes', not 'children'."""
    node = Pdf.stack(nodes=[Pdf.text(NoAttr, ["x"])])
    d = node.to_dict()
    assert "nodes" in d
    assert "children" not in d
