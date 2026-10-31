"""The builders write the schema's names, and what they build renders like the XML it converts to."""
import re

import pytest

from lpdf import (
    L, LMarkdown, NoAttr, PdfEngine, EngineException,
    MarkdownAttr, MarkdownH1Attr, MarkdownQuoteAttr, MarkdownStylesAttr,
    BarcodeAtAttr, BarcodeAttr, BookmarkAttr, BuiltinFont, CodeAttr, CodeSpanAttr, ImgAtAttr, ListAttr, TextAtAttr, CircleAttr, DocumentAssets, DocumentAttr, DocumentTokens, EllipseAttr,
    FieldAttr, FieldType, FileAttr, FileRelationship, FontAttr, FootnoteCounter, ImageAttr, ImgAttr, LayerAttr, LineAttr, LinkAttr, Orientation, PathAttr, Permission, Pin,
    RectAttr, RegionAttr, RowAttr, SectionAttr, SectionType, ShapeAttr, SpanAttr, TableAttr, TdAttr, TrAttr, ColumnAttr, FrameAttr, GridAttr, TextAttr, Transform,
)
from lpdf.layout.text_node import TextNode


def _normalised(pdf: bytes) -> bytes:
    text = pdf.decode("latin-1")
    text = re.sub(r"/CreationDate[^\n]*", "", text)
    text = re.sub(r"/ID *\[[^\]]*\]", "", text)
    return text.encode("latin-1")


def _render(input) -> bytes:
    return _normalised(PdfEngine().set_license_key("test-key").render(input))


def _in_layout(*nodes) -> object:
    return L.document(NoAttr, [L.section(NoAttr, [L.layout(NoAttr, list(nodes))])])


# ── Attribute types ────────────────────────────────────────────────────────────

@pytest.mark.parametrize(("node", "says"), [
    (lambda: L.grid(GridAttr(cols="3"), [L.text(NoAttr, ["a"])]), r'grid: cols must be a whole number from 1 to 12, not "3"'),
    (lambda: L.text(TextAttr(bold="true"), ["a"]), r'text: bold must be true or false, not "true"'),
    (lambda: L.text(TextAttr(bold=1), ["a"]), r"text: bold must be true or false, not 1"),
    (lambda: L.column(ColumnAttr(opacity="0.5")), r'column: opacity must be a number from 0 to 1, not "0.5"'),
    (lambda: L.text(TextAttr(line_height="1.5"), ["a"]), r'text: line-height must be a name or a number above 0, not "1.5"'),
    (lambda: L.grid(GridAttr(cols=3.5), [L.text(NoAttr, ["a"])]), r"grid: cols must be a whole number from 1 to 12, not 3.5"),
])
def test_the_engine_refuses_a_value_of_the_wrong_type_when_it_renders(node, says):
    with pytest.raises(EngineException, match=says):
        PdfEngine().set_license_key("test-key").render(_in_layout(node()))


@pytest.mark.parametrize(("build", "says"), [
    (lambda: L.column(ColumnAttr(opacity=float("nan"))), r"^opacity must be a finite number, not nan$"),
    (lambda: L.text(TextAttr(line_height=float("inf")), ["a"]), r"^line-height must be a finite number, not inf$"),
    # A string attribute too: as text, a missing title from pandas would be a bookmark named nan.
    (lambda: L.bookmark(BookmarkAttr(label=float("nan"))), r"^label must be a finite number, not nan$"),
    (lambda: L.document(DocumentAttr(tokens=DocumentTokens(line_height={"m": float("nan")}))),
     r"^tokens\.line_height\.m must be a finite number, not nan$"),
    (lambda: L.document(DocumentAttr(tokens=DocumentTokens(gradients={"fade": {"type": "linear", "angle": float("-inf")}}))),
     r"^tokens\.gradients\.fade\.angle must be a finite number, not -inf$"),
])
def test_a_number_a_document_cannot_hold_is_refused_when_it_is_built(build, says):
    with pytest.raises(ValueError, match=says):
        build()


def test_an_attribute_the_element_does_not_have_is_refused_by_the_class_and_by_the_engine():
    with pytest.raises(TypeError, match="colr"):
        TextAttr(colr="red")  # type: ignore[call-arg]
    # A node built around the class, as a tree from elsewhere would be.
    with pytest.raises(EngineException, match=r"text: unknown attribute 'colr' — expected font-size, font, bold, color,"):
        PdfEngine().set_license_key("test-key").render(_in_layout(TextNode({"colr": "red"}, ["a"])))


def test_a_whole_number_given_as_a_float_renders_as_the_whole_number():
    # json.dumps writes a float such as 6 / 2 as 3.0.
    as_float = _in_layout(L.grid(GridAttr(cols=6 / 2), [L.text(NoAttr, ["a"]), L.text(NoAttr, ["b"])]))
    xml = ('<lpdf version="1"><document><section><layout><grid cols="3">'
           "<text>a</text><text>b</text></grid></layout></section></document></lpdf>")
    no_cols = _in_layout(L.grid(NoAttr, [L.text(NoAttr, ["a"]), L.text(NoAttr, ["b"])]))
    assert _render(as_float) == _render(xml)
    assert _render(as_float) != _render(no_cols)


def test_a_typed_value_renders_as_its_text_does_in_xml():
    built = _in_layout(L.grid(GridAttr(cols=2, opacity=0.5), [
        L.text(TextAttr(bold=True, line_height=1.5), ["a"]), L.text(TextAttr(line_height="l"), ["b"]),
    ]))
    xml = ('<lpdf version="1"><document><section><layout><grid cols="2" opacity="0.5">'
           '<text bold="true" line-height="1.5">a</text><text line-height="l">b</text></grid></layout></section></document></lpdf>')
    assert _render(built) == _render(xml)


# ── Attribute names ────────────────────────────────────────────────────────────

def test_text_align_and_bold_use_the_schema_names():
    node = L.text(TextAttr(align="right", bold=True), ["x"])
    assert node.to_dict()["attrs"] == {"align": "right", "bold": True}


def test_link_and_span_carry_href():
    assert L.link(LinkAttr(href="https://lpdf.io")).to_dict()["attrs"] == {"href": "https://lpdf.io"}
    assert L.span(SpanAttr(href="https://lpdf.io"), ["x"]).to_dict()["attrs"] == {"href": "https://lpdf.io"}


def test_field_carries_its_type_and_name_as_attributes():
    node = L.field(FieldAttr(type="text", name="email", max_len=40, action_url="https://lpdf.io"))
    assert node.to_dict()["attrs"] == {
        "type": "text", "name": "email", "max-len": 40, "action-url": "https://lpdf.io",
    }


def test_a_required_attribute_cannot_be_left_out():
    with pytest.raises(TypeError):
        LinkAttr()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        FieldAttr(type="text")  # type: ignore[call-arg]


def test_region_is_written_as_region():
    node = L.region(RegionAttr(pin="top"), [L.text(NoAttr, ["header"])])
    assert node.to_dict()["type"] == "region"
    assert node.to_dict()["attrs"] == {"pin": "top"}


def test_document_font_and_debug_are_written():
    doc = L.document(DocumentAttr(font="Times-Roman", debug=True))
    assert doc.to_dict()["attrs"] == {"font": "Times-Roman", "debug": True}


# ── Canvas ─────────────────────────────────────────────────────────────────────

def test_rect_writes_its_attributes_as_given():
    node = L.rect(RectAttr(width="100pt", height="60pt", x="10pt", y="20pt", fill="#ff0000", radius="6pt"))
    assert node.to_dict() == {
        "type": "rect",
        "attrs": {"width": "100pt", "height": "60pt", "x": "10pt", "y": "20pt", "fill": "#ff0000", "radius": "6pt"},
    }


def test_canvas_primitives_use_their_schema_names():
    assert L.line(LineAttr(x1="0pt", y1="0pt", x2="9pt", y2="9pt", line_cap="round")).to_dict()["type"] == "line"
    assert L.circle(CircleAttr(r="5pt", x="1pt", y="1pt")).to_dict()["type"] == "circle"
    assert L.ellipse(EllipseAttr(rx="5pt", ry="3pt")).to_dict()["type"] == "ellipse"
    path = L.path(PathAttr(d="M 0 0 L 9 9", fill_rule="evenodd")).to_dict()
    assert path == {"type": "path", "attrs": {"d": "M 0 0 L 9 9", "fill-rule": "evenodd"}}
    assert L.img_at(ImgAtAttr(name="logo", width="10pt", height="10pt")).to_dict()["type"] == "img-at"


def test_layer_shapes_are_sized_by_width_and_height_and_placed_by_x_and_y():
    for attrs in (RectAttr, ImgAtAttr, TextAtAttr):
        assert "w" not in attrs.__dataclass_fields__
        assert "width" in attrs.__dataclass_fields__
    assert "h" not in RectAttr.__dataclass_fields__
    assert "height" in RectAttr.__dataclass_fields__
    for attrs in (CircleAttr, EllipseAttr):
        assert "cx" not in attrs.__dataclass_fields__ and "cy" not in attrs.__dataclass_fields__
        assert "x" in attrs.__dataclass_fields__ and "y" in attrs.__dataclass_fields__


def test_a_barcode_at_is_written_under_its_element_name():
    d = L.barcode_at(BarcodeAtAttr(type="qr", data="x", x="10pt", y="20pt", width="60pt")).to_dict()
    assert d == {"type": "barcode-at", "attrs": {"type": "qr", "data": "x", "x": "10pt", "y": "20pt", "width": "60pt"}}


def test_a_text_at_writes_its_line_limits_under_the_schema_names():
    d = L.text_at(TextAtAttr(x="0pt", y="0pt", width="80pt", max_lines=2, ellipsis=True, line_height=1.5), ["Hi"]).to_dict()
    assert d["attrs"]["max-lines"] == 2
    assert d["attrs"]["ellipsis"] is True
    assert d["attrs"]["line-height"] == 1.5


def test_a_text_that_captures_and_one_that_shows_a_capture_use_the_schema_names():
    assert L.text(TextAttr(capture="chapter"), ["x"]).to_dict()["attrs"] == {"capture": "chapter"}
    sink = L.text(TextAttr(capture_ref="chapter", capture_mode="first", capture_fallback="None"), [])
    assert sink.to_dict()["attrs"] == {"capture-ref": "chapter", "capture-mode": "first", "capture-fallback": "None"}


def test_a_barcode_is_sized_by_width_and_height_not_by_size():
    assert "size" not in BarcodeAttr.__dataclass_fields__
    assert "width" in BarcodeAttr.__dataclass_fields__
    assert "height" in BarcodeAttr.__dataclass_fields__


def test_canvas_text_takes_attributes_first_and_content_second():
    node = L.text_at(
        TextAtAttr(x="10pt", y="20pt", font_size="12pt"),
        ["base ", L.span(SpanAttr(font="Helvetica-Bold"), ["bold"])],
    )
    d = node.to_dict()
    assert d["type"] == "text-at"
    assert d["attrs"] == {"x": "10pt", "y": "20pt", "font-size": "12pt"}
    assert d["nodes"][0] == "base "
    assert d["nodes"][1] == {"type": "span", "attrs": {"font": "Helvetica-Bold"}, "nodes": ["bold"]}


def test_layer_attributes_are_written_as_given():
    node = L.layer(LayerAttr(page="first", opacity=0.5, transform="rotate(45 100 100)"))
    assert node.to_dict() == {
        "type": "layer",
        "attrs": {"page": "first", "opacity": 0.5, "transform": "rotate(45 100 100)"},
        "nodes": [],
    }


def test_a_transform_is_a_string_a_layer_accepts():
    assert str(Transform.translate(10, 20)) == "matrix(1.0,0.0,0.0,1.0,10,20)"


# ── Rendering ──────────────────────────────────────────────────────────────────

def _built_document():
    return L.document(DocumentAttr(size="a4"), [
        L.section(NoAttr, [
            L.layout(NoAttr, [
                L.column(ColumnAttr(gap="12pt"), [
                    L.text(TextAttr(align="right", bold=True), ["Title"]),
                    L.text(NoAttr, ["Body ", L.span(SpanAttr(bold=True), ["bold"]), " text"]),
                    L.link(LinkAttr(href="https://lpdf.io"), [L.text(NoAttr, ["link"])]),
                ]),
            ]),
            L.layer(LayerAttr(page="each"), [
                L.rect(RectAttr(x="40pt", y="40pt", width="100pt", height="60pt", fill="#ff0000", radius="6pt")),
                L.text_at(TextAtAttr(x="40pt", y="120pt", font_size="10pt"),
                          ["Layer ", L.span(SpanAttr(color="#0000ff"), ["text"])]),
            ]),
        ]),
    ])


def test_an_alias_is_the_slot_it_names_and_renders_the_same_from_the_builder_and_its_xml():
    def build(size: str):
        return L.document(
            DocumentAttr(tokens=DocumentTokens(aliases={"caption": "xs", "heading": "xl"})),
            [L.section(None, [L.layout(None, [L.text(TextAttr(font_size=size), ["Sized"])])])],
        )

    caption = build("caption")
    pdf = _render(caption)
    assert pdf == _render(L.to_xml(caption))
    assert pdf == _render(build("xs"))
    assert pdf != _render(build("heading"))


def test_a_name_that_is_neither_a_slot_nor_an_alias_is_rejected():
    built = L.document(
        DocumentAttr(tokens=DocumentTokens(aliases={"caption": "xs"})),
        [L.section(None, [L.layout(None, [L.text(TextAttr(font_size="medum"), ["Sized"])])])],
    )
    with pytest.raises(EngineException, match=r"invalid text size: 'medum': expected a slot from xs to xxl, an alias \(caption\)"):
        PdfEngine().set_license_key("test-key").render(built)


def test_a_height_is_the_slot_it_names_and_renders_the_same_from_the_builder_and_its_xml():
    def build(height: str, row: dict | None = None):
        return L.document(
            DocumentAttr(tokens=DocumentTokens(height=row)) if row else None,
            [L.section(None, [L.layout(None, [L.column(ColumnAttr(background="#cccccc", height=height))])])],
        )

    slot = build("m")
    pdf = _render(slot)
    assert pdf == _render(L.to_xml(slot))
    assert pdf == _render(build("32pt"))
    assert pdf != _render(build("xl"))

    row = {"xs": "10pt", "s": "20pt", "m": "50pt", "l": "60pt", "xl": "70pt", "xxl": "80pt"}
    assert _render(build("m", row)) == _render(build("50pt"))


def test_a_height_that_is_not_a_slot_a_length_fill_or_full_is_rejected():
    built = L.document(None, [L.section(None, [L.layout(None, [L.column(ColumnAttr(height="medum"))])])])
    with pytest.raises(EngineException, match=r"invalid height value: 'medum' — expected full, fill, a slot from xs to xxl or a pt value"):
        PdfEngine().set_license_key("test-key").render(built)


def test_a_shape_has_the_attributes_of_its_type_under_the_schema_names():
    node = L.shape(ShapeAttr(
        type="rect", width="14pt", height="m", radius="2pt", fill="primary",
        stroke="#000000", stroke_width="1pt", stroke_dash="3 2", opacity=0.5,
    ))
    assert node.to_dict() == {"type": "shape", "attrs": {
        "type": "rect", "width": "14pt", "height": "m", "radius": "2pt", "fill": "primary",
        "stroke": "#000000", "stroke-width": "1pt", "stroke-dash": "3 2", "opacity": 0.5,
    }}
    assert L.shape(ShapeAttr(type="circle", r="5pt")).to_dict()["attrs"] == {"type": "circle", "r": "5pt"}


def test_a_shape_of_each_type_is_drawn_and_renders_the_same_from_the_builder_and_its_xml():
    def build(*shapes):
        return L.document(None, [L.section(None, [L.layout(None, [
            L.row(RowAttr(align="center"), [*shapes, L.text(None, ["After"])]),
        ])])])

    without = _render(build())
    for shape in [
        L.shape(ShapeAttr(type="rect", width="60pt", height="12pt", fill="#00aa00")),
        L.shape(ShapeAttr(type="circle", r="8pt", fill="#00aa00")),
        L.shape(ShapeAttr(type="ellipse", width="40pt", height="20pt", fill="#00aa00")),
    ]:
        document = build(shape)
        pdf = _render(document)
        assert pdf != without
        assert pdf == _render(L.to_xml(document))


def test_a_footnote_is_an_fn_child_of_a_text_and_the_counter_is_an_attribute_of_the_document_and_a_section():
    text = L.text(None, ["Total", L.fn(NoAttr, ["See ", L.span(SpanAttr(bold=True), ["this"]), "."]), " here"])
    document = L.document(
        DocumentAttr(footnote_counter=FootnoteCounter.DOCUMENT),
        [L.section(SectionAttr(footnote_counter=FootnoteCounter.PAGE), [L.layout(None, [text])])],
    )
    xml = L.to_xml(document)
    assert re.search(r'<document [^>]*footnote-counter="document"', xml), xml
    assert re.search(r'<section [^>]*footnote-counter="page"', xml), xml
    assert '<text>Total<fn>See <span bold="true">this</span>.</fn> here</text>' in xml
    assert L.fn(NoAttr, ["a"]).to_dict() == {"type": "fn", "attrs": {}, "nodes": ["a"]}


def test_a_code_and_a_code_span_are_written_as_their_elements_and_render_the_same_from_the_builder_and_its_xml():
    document = L.document(None, [L.section(None, [L.layout(None, [
        L.code(CodeAttr(tab_size=2), ["\nfn a() {\n\tb(", L.span(SpanAttr(color="#c0392b"), ["x"]), ");\n}\n"]),
        L.text(None, ["Run ", L.code_span(CodeSpanAttr(background="#ffff00"), ["cargo test"]), " now"]),
    ])])])

    xml = L.to_xml(document)
    assert '<code tab-size="2">\nfn a() {\n\tb(<span color="#c0392b">x</span>);\n}\n</code>' in xml, xml
    assert 'Run <code-span background="#ffff00">cargo test</code-span> now' in xml, xml
    assert L.code().to_dict()["type"] == "code"
    assert L.code_span().to_dict()["type"] == "code-span"
    assert _render(document) == _render(xml)


def test_a_code_keeps_its_spaces_and_one_longer_than_a_page_goes_on_in_the_next_and_a_bad_tab_size_is_rejected():
    def build(*nodes):
        return L.document(None, [L.section(None, [L.layout(None, [L.code(None, list(nodes))])])])

    assert _render(build("a    b")) != _render(build("a b"))

    lines = "\n".join(f"line {i}" for i in range(1, 151))
    assert len(re.findall(rb"/Type\s*/Page[^s]", _render(build(lines)))) >= 2, "the code splits across pages"

    bad = L.document(None, [L.section(None, [L.layout(None, [L.code(CodeAttr(tab_size=0), ["x"])])])])
    with pytest.raises(EngineException, match=r"tab-size must be a whole number from 1 to 16, not 0"):
        PdfEngine().set_license_key("test-key").render(bad)


def test_a_list_is_written_with_its_items_and_renders_the_same_from_the_builder_and_its_xml():
    document = L.document(None, [L.section(None, [L.layout(None, [
        L.list(ListAttr(type="number", format="lower-alpha", suffix=")"), [
            L.li(None, [L.text(None, ["One"])]),
            L.li(None, [L.text(None, ["Two"]), L.list(ListAttr(bullet="dash"), [L.li(None, [L.text(None, ["Nested"])])])]),
        ]),
    ])])])

    xml = L.to_xml(document)
    assert re.search(r'<list format="lower-alpha" suffix="\)" type="number">\s*<li>\s*<text>One</text>\s*</li>', xml), xml
    assert re.search(r'<list bullet="dash">\s*<li>\s*<text>Nested</text>', xml), xml
    assert L.list().to_dict()["type"] == "list"
    assert L.li().to_dict()["type"] == "li"
    assert _render(document) == _render(xml)


def test_a_number_list_writes_its_numbers_and_a_bullet_list_refuses_what_numbers_them():
    def build(attrs):
        items = [L.li(None, [L.text(None, ["A"])]), L.li(None, [L.text(None, ["B"])])]
        return L.document(None, [L.section(None, [L.layout(None, [L.list(attrs, items)])])])

    bullets = _render(build(None))
    numbers = _render(build(ListAttr(type="number")))
    roman = _render(build(ListAttr(type="number", format="lower-roman", start=3)))
    assert bullets != numbers
    assert numbers != roman

    with pytest.raises(EngineException, match=r"numbers the items of a list"):
        PdfEngine().set_license_key("test-key").render(build(ListAttr(format="lower-alpha")))


def test_a_footnote_is_drawn_and_renders_the_same_from_the_builder_and_its_xml_and_one_in_a_table_is_rejected():
    def build(*nodes):
        return L.document(None, [L.section(None, [L.layout(None, [L.text(None, ["Total", *nodes, " here"])])])])

    without = _render(build())
    noted = build(L.fn(NoAttr, ["The note."]))
    assert _render(noted) != without
    assert _render(noted) == _render(L.to_xml(noted))

    def counted(counter):
        return L.document(DocumentAttr(footnote_counter=counter), [
            L.section(None, [L.layout(None, [L.text(None, ["One", L.fn(NoAttr, ["A."])])])]),
            L.section(None, [L.layout(None, [L.text(None, ["Two", L.fn(NoAttr, ["B."])])])]),
        ])
    assert _render(counted(FootnoteCounter.DOCUMENT)) != _render(counted(FootnoteCounter.SECTION))

    table = L.document(None, [L.section(None, [L.layout(None, [
        L.table(TableAttr(cols="1fr"), [L.tr(None, [L.td(None, [L.text(None, ["x", L.fn(NoAttr, ["y"])])])])]),
    ])])])
    with pytest.raises(EngineException, match=r"<fn> is not supported in a table"):
        PdfEngine().set_license_key("test-key").render(table)


def test_a_kept_table_row_moves_on_with_the_row_after_it_and_renders_the_same_from_the_builder_and_its_xml():
    # The table starts 30pt above the foot of the page, so rows A and B fit and C does not.
    def build(keep: TrAttr | None):
        return L.document(None, [L.section(None, [L.layout(None, [
            L.frame(FrameAttr(height="739pt")),
            L.table(TableAttr(cols="1fr"), [
                L.tr(None, [L.td(None, [L.text(None, ["A"])])]),
                L.tr(keep, [L.td(None, [L.text(None, ["B"])])]),
                L.tr(None, [L.td(None, [L.text(None, ["C"])])]),
            ]),
        ])])])

    kept = build(TrAttr(keep="with-next"))
    assert L.tr(TrAttr(keep="with-next")).to_dict()["attrs"] == {"keep": "with-next"}
    assert _render(kept) != _render(build(None))
    assert _render(kept) == _render(L.to_xml(kept))


def test_a_table_cell_that_spans_columns_moves_the_cells_after_it_and_renders_the_same_from_the_builder_and_its_xml():
    def build(first: TdAttr | None):
        return L.document(None, [L.section(None, [L.layout(None, [
            L.table(TableAttr(cols="1fr 1fr 1fr"), [
                L.tr(None, [L.td(first, [L.text(None, ["A"])]), L.td(None, [L.text(None, ["B"])])]),
            ]),
        ])])])

    spanning = build(TdAttr(colspan=2))
    assert L.td(TdAttr(colspan=2)).to_dict()["attrs"] == {"colspan": 2}
    assert _render(spanning) != _render(build(None))
    assert _render(spanning) == _render(L.to_xml(spanning))
    with pytest.raises(EngineException, match=r"span 4 columns, but the table has 3"):
        _render(build(TdAttr(colspan=3)))


def test_a_table_cell_that_spans_rows_moves_the_cells_under_it_and_renders_the_same_from_the_builder_and_its_xml():
    def build(first: TdAttr | None):
        return L.document(None, [L.section(None, [L.layout(None, [
            L.table(TableAttr(cols="1fr 1fr"), [
                L.tr(None, [L.td(first, [L.text(None, ["A"])]), L.td(None, [L.text(None, ["B"])])]),
                L.tr(None, [L.td(None, [L.text(None, ["C"])])]),
            ]),
        ])])])

    spanning = build(TdAttr(rowspan=2))
    assert L.td(TdAttr(rowspan=2)).to_dict()["attrs"] == {"rowspan": 2}
    assert _render(spanning) != _render(build(None))
    assert _render(spanning) == _render(L.to_xml(spanning))
    with pytest.raises(EngineException, match=r"a rowspan that runs 1 row past the last row of the table"):
        _render(build(TdAttr(rowspan=3)))


def test_a_circle_without_r_is_rejected_and_says_so():
    built = L.document(None, [L.section(None, [L.layout(None, [L.shape(ShapeAttr(type="circle"))])])])
    with pytest.raises(EngineException, match=r"a circle needs 'r'"):
        PdfEngine().set_license_key("test-key").render(built)


def test_a_gradient_of_the_tokens_fills_a_box_and_renders_the_same_from_the_builder_and_its_xml():
    def build(background: str):
        return L.document(
            DocumentAttr(tokens=DocumentTokens(gradients={
                "fade": {"type": "linear", "from": "#ff0000", "to": "#0000ff", "angle": 90},
            })),
            [L.section(None, [L.layout(None, [L.column(ColumnAttr(background=background, height="60pt"))])])],
        )

    gradient = build("gradient:fade")
    pdf = _render(gradient)
    assert pdf == _render(L.to_xml(gradient))
    assert pdf != _render(build("#336699"))
    assert b"/ShadingType 2" in pdf


def test_a_built_document_renders_the_same_as_its_xml():
    built = _built_document()
    assert _render(built) == _render(L.to_xml(built))


def test_bold_text_is_the_bold_face_of_the_font():
    def doc(attrs: str) -> str:
        return (f'<lpdf version="1"><document><section><layout><text {attrs}>Hello</text>'
                "</layout></section></document></lpdf>")

    assert _render(doc('bold="true"')) == _render(doc('font="Helvetica-Bold"'))
    assert _render(doc('bold="true"')) != _render(doc(""))


# ── Bookmarks and the table of contents ────────────────────────────────────────

def test_a_bookmark_goes_in_a_layout_and_directly_in_a_section():
    bookmark = L.bookmark(BookmarkAttr(label="Methods", level=2, id="methods"))
    assert bookmark.to_dict() == {"type": "bookmark", "attrs": {"label": "Methods", "level": 2, "id": "methods"}}

    section = L.section(SectionAttr(type=SectionType.TOC, toc_indent_step="14pt"), [
        L.bookmark(BookmarkAttr(label="Contents")),
        L.layout(NoAttr, []),
    ]).to_dict()
    assert section["attrs"] == {"type": "toc", "toc-indent-step": "14pt"}
    assert section["nodes"][0]["type"] == "bookmark"


def test_bookmarks_fill_the_outline_and_render_like_their_xml():
    built = L.document(NoAttr, [
        L.section(NoAttr, [L.bookmark(BookmarkAttr(label="Cover")), L.layout(NoAttr, [L.text(NoAttr, ["Cover"])])]),
        L.section(NoAttr, [
            L.layout(NoAttr, [
                L.link(LinkAttr(href="#methods"), [L.text(NoAttr, ["Go to Methods"])]),
                L.bookmark(BookmarkAttr(label="Methods")),
                L.text(NoAttr, ["Methods"]),
            ]),
        ]),
    ])
    pdf = _render(built)
    assert b"/Title (Cover)" in pdf and b"/Title (Methods)" in pdf
    assert b"/D /methods" in pdf
    assert pdf == _render(L.to_xml(built))


# ── Assets ─────────────────────────────────────────────────────────────────────

_PIXEL = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8cfc0f01f0005000101"
    "0eabb4630000000049454e44ae426082")


def _document_with_assets(assets: DocumentAssets, *nodes) -> object:
    return L.document(DocumentAttr(assets=assets), [L.section(NoAttr, [L.layout(NoAttr, list(nodes))])])


def test_assets_declare_fonts_and_images_with_the_schema_names():
    assets = DocumentAssets(
        fonts=[FontAttr(name="heading", core=BuiltinFont.TIMES_BOLD)],
        images=[ImageAttr(name="logo", ref="company-logo", src="logo.png")],
    )
    assert L.document(DocumentAttr(assets=assets)).to_dict()["attrs"]["assets"] == {
        "fonts": [{"name": "heading", "core": "Times-Bold"}],
        "images": [{"name": "logo", "ref": "company-logo", "src": "logo.png"}],
    }
    assert L.assets(assets) is assets


def test_an_asset_needs_a_name():
    with pytest.raises(TypeError):
        FontAttr(core="Helvetica")  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        ImageAttr(src="logo.png")  # type: ignore[call-arg]


def test_a_font_declared_in_the_assets_is_the_font_the_text_is_set_in():
    built = _document_with_assets(
        DocumentAssets(fonts=[FontAttr(name="heading", core=BuiltinFont.TIMES_BOLD)]),
        L.text(TextAttr(font="heading"), ["Hello"]),
    )
    engine = PdfEngine().set_license_key("test-key")
    assert b"/BaseFont /Times-Bold" in engine.render(built)
    assert _render(built) == _render(L.to_xml(built))


def test_an_image_declared_in_the_assets_can_be_used_and_renders_the_same_as_its_xml():
    built = _document_with_assets(
        DocumentAssets(images=[ImageAttr(name="logo")]),
        L.img(ImgAttr(name="logo", width="40pt")),
    )
    engine = PdfEngine().set_license_key("test-key").load_image("logo", _PIXEL)
    assert _normalised(engine.render(built)) == _normalised(engine.render(L.to_xml(built)))


def test_a_section_with_two_layouts_is_rejected():
    built = L.document(DocumentAttr(), [L.section(NoAttr, [
        L.layout(NoAttr, [L.text(NoAttr, ["a"])]),
        L.layout(NoAttr, [L.text(NoAttr, ["b"])]),
    ])])
    with pytest.raises(EngineException, match="at most one <layout>"):
        PdfEngine().set_license_key("test-key").render(built)


def test_an_image_used_but_not_declared_in_the_assets_is_an_error_that_names_it():
    built = L.document(DocumentAttr(), [L.section(NoAttr, [L.layout(NoAttr, [L.img(ImgAttr(name="ghost"))])])])
    engine = PdfEngine().set_license_key("test-key").load_image("ghost", _PIXEL)
    with pytest.raises(EngineException, match="ghost"):
        engine.render(built)


def test_an_image_declared_with_a_src_is_read_from_there(tmp_path):
    image = tmp_path / "logo.png"
    image.write_bytes(_PIXEL)
    built = _document_with_assets(
        DocumentAssets(images=[ImageAttr(name="logo", src=str(image))]),
        L.img(ImgAttr(name="logo", width="40pt")),
    )
    assert PdfEngine().set_license_key("test-key").render(built).startswith(b"%PDF-")


def _document_with_attachments(*files: FileAttr):
    return L.document(DocumentAttr(attachments=list(files)), [
        L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Invoice"])])]),
    ])


def test_a_file_the_document_carries_is_embedded_from_load_file_or_its_src(tmp_path):
    terms = tmp_path / "terms.txt"
    terms.write_text("Terms of sale")
    built = _document_with_attachments(
        FileAttr(name="invoice.xml", ref="invoice", mime="text/xml", relationship=FileRelationship.DATA),
        FileAttr(name="terms.txt", src=str(terms), description="The terms"),
    )
    engine = PdfEngine().set_license_key("test-key").load_file("invoice", b"<invoice/>")
    pdf = engine.render(built)
    assert pdf.count(b"/Type /EmbeddedFile") == 2
    assert b"/AFRelationship /Data" in pdf
    assert b"/Subtype /text#2Fxml" in pdf
    assert _normalised(pdf) == _normalised(engine.render(L.to_xml(built)))


def test_the_src_of_a_file_is_read_as_the_engine_reads_its_xml(tmp_path):
    terms = tmp_path / "R&D terms.txt"
    terms.write_text("Terms")
    built = _document_with_attachments(FileAttr(name="Terms & Conditions.txt", src=str(terms), description="Rows > 100"))
    xml = L.to_xml(built).replace(
        "<attachments>", '<attachments><!-- <file name="old.csv" src="/no/such/old.csv"/> -->')
    engine = PdfEngine().set_license_key("test-key")
    assert engine.render(xml).count(b"/Type /EmbeddedFile") == 1
    assert _normalised(engine.render(built)) == _normalised(engine.render(xml))

    plain = tmp_path / "terms.txt"
    plain.write_text("Terms")
    quoted = (f"<lpdf version='1'><document><attachments><file name='t.txt' src='{plain}'/></attachments>"
              "<section><layout><text>x</text></layout></section></document></lpdf>")
    assert b"/Type /EmbeddedFile" in engine.render(quoted)


def test_a_file_whose_src_cannot_be_read_is_an_error_that_names_it():
    built = _document_with_attachments(FileAttr(name="data.csv", src="/no/such/data.csv"))
    with pytest.raises(EngineException, match=r"file 'data\.csv'.*/no/such/data\.csv"):
        PdfEngine().set_license_key("test-key").render(built)


def test_a_file_with_no_bytes_is_an_error_that_says_how_to_load_it():
    xml = ('<lpdf version="1"><document><attachments><file name="a.xml"/></attachments>'
           '<section><layout><text>x</text></layout></section></document></lpdf>')
    with pytest.raises(EngineException, match=r"loadFile\('a\.xml', bytes\)"):
        PdfEngine().set_license_key("test-key").render(xml)


def test_the_constants_are_the_schema_values():
    assert FileRelationship.DATA == "data"
    assert FieldType.TEXT == "text"
    assert Pin.TOP == "top"
    assert Orientation.LANDSCAPE == "landscape"
    assert BuiltinFont.TIMES_BOLD == "Times-Bold"
    assert Permission.ALL == "all"


# ── Markdown ───────────────────────────────────────────────────────────────────

MARKDOWN_BODY = "# Release notes\n\nSome *emphasis*, **strong** text and `code`.\n\n- one\n- two\n\n> a quote\n"


def _markdown_document(attrs=None, styles=None, text=MARKDOWN_BODY):
    parts = ([styles] if styles is not None else []) + [LMarkdown.content(NoAttr, [text])]
    return L.document(None, [L.section(None, [L.markdown(attrs, parts)])])


def test_a_markdown_its_styles_its_content_and_their_rules_are_built_with_the_schema_names():
    markdown = L.markdown(MarkdownAttr(margin="54pt", gap="m", bookmarks=2)).to_dict()
    assert markdown["type"] == "markdown"
    assert markdown["attrs"] == {"margin": "54pt", "gap": "m", "bookmarks": 2}

    styles = LMarkdown.styles(MarkdownStylesAttr(src="styles.xml"), [LMarkdown.h1(MarkdownH1Attr(font_size="xl", color="muted"))]).to_dict()
    assert styles["type"] == "markdown-styles"
    assert styles["attrs"] == {"src": "styles.xml"}
    assert styles["nodes"] == [{"type": "h1", "attrs": {"font-size": "xl", "color": "muted"}}]
    assert LMarkdown.quote(MarkdownQuoteAttr(bar_color="primary")).to_dict()["attrs"] == {"bar-color": "primary"}
    assert LMarkdown.em().to_dict() == {"type": "em", "attrs": {}}
    assert LMarkdown.del_().to_dict()["type"] == "del"
    assert LMarkdown.content(NoAttr, ["# a"]).to_dict()["nodes"] == ["# a"]


def test_a_markdown_is_written_as_xml_with_its_markdown_as_it_is_and_renders_the_same_from_the_builder_and_its_xml():
    document = _markdown_document(
        MarkdownAttr(gap="8pt"),
        LMarkdown.styles(NoAttr, [LMarkdown.h1(MarkdownH1Attr(color="#ff0000"))]),
        "a < b & c ]]> d\n\n    code\n",
    )
    xml = L.to_xml(document)
    assert '<markdown gap="8pt">' in xml
    assert re.search(r'<markdown-styles>\s*<h1 color="#ff0000"\s*/>\s*</markdown-styles>', xml)
    assert "<markdown-content><![CDATA[a < b & c ]]]]><![CDATA[> d" in xml
    assert _render(document) == _render(xml)


def test_a_markdown_renders_the_text_it_is_given_and_a_rule_that_sets_a_color_changes_the_page():
    plain = _render(_markdown_document())
    assert plain.startswith(b"%PDF-")
    assert plain != _render(_markdown_document(styles=LMarkdown.styles(NoAttr, [LMarkdown.h1(MarkdownH1Attr(color="#ff0000"))])))
    assert plain != _render(_markdown_document(text="# Another title"))


def test_a_file_of_rules_is_read_from_the_src_of_its_styles_or_loaded_by_name(tmp_path):
    file = tmp_path / "styles.xml"
    file.write_text('<markdown-styles><h1 color="#ff0000"/></markdown-styles>', encoding="utf-8")
    inline = _render(_markdown_document(styles=LMarkdown.styles(NoAttr, [LMarkdown.h1(MarkdownH1Attr(color="#ff0000"))])))
    from_src = _markdown_document(styles=LMarkdown.styles(MarkdownStylesAttr(src=str(file))))
    assert _render(from_src) == inline
    assert _render(L.to_xml(from_src)) == inline

    engine = PdfEngine().set_license_key("test-key").load_markdown_styles("theme.xml", '<markdown-styles><h1 color="#ff0000"/></markdown-styles>')
    loaded = engine.render(_markdown_document(styles=LMarkdown.styles(MarkdownStylesAttr(src="theme.xml"))))
    assert _normalised(loaded) == inline


def test_a_file_of_rules_that_is_not_there_is_an_error_that_names_the_src():
    with pytest.raises(EngineException, match="missing-styles.xml"):
        _render(_markdown_document(styles=LMarkdown.styles(MarkdownStylesAttr(src="missing-styles.xml"))))


def test_raw_html_is_left_out_of_the_markdown_and_the_words_in_it_are_kept():
    with_html = _render(_markdown_document(text="fine\n\n<div>kept</div>\n"))
    assert with_html == _render(_markdown_document(text="fine\n\nkept\n"))


def test_the_markdown_comes_from_the_data_of_an_xml_document_or_the_text_written_in_it():
    xml = '<lpdf version="1"><document><section><markdown><markdown-content data-value="body"><![CDATA[# From the text]]></markdown-content></markdown></section></document></lpdf>'
    engine = PdfEngine().set_license_key("test-key")
    from lpdf import RenderOptions
    from_data = _normalised(engine.render(xml, RenderOptions(data={"body": "# From the data"})))
    from_text = _normalised(engine.render(xml))
    assert from_data != from_text
