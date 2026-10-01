"""The builders write the schema's names, and what they build renders like the XML it converts to."""
import re

import pytest

from lpdf import (
    L, NoAttr, PdfEngine, EngineException,
    BuiltinFont, CanvasImgAttr, CanvasTextAttr, CircleAttr, DocumentAssets, DocumentAttr, EllipseAttr, FieldAttr,
    FieldType, FontAttr, ImageAttr, ImgAttr, LayerAttr, LineAttr, LinkAttr, Orientation, PathAttr, Pin, RectAttr,
    RegionAttr, SpanAttr, StackAttr, TextAttr, Transform,
)


def _normalised(pdf: bytes) -> bytes:
    text = pdf.decode("latin-1")
    text = re.sub(r"/CreationDate[^\n]*", "", text)
    text = re.sub(r"/ID *\[[^\]]*\]", "", text)
    return text.encode("latin-1")


def _render(input) -> bytes:
    return _normalised(PdfEngine().set_license_key("test-key").render(input))


# ── Attribute names ────────────────────────────────────────────────────────────

def test_text_align_and_bold_use_the_schema_names():
    node = L.text(TextAttr(align="right", bold="true"), ["x"])
    assert node.to_dict()["attrs"] == {"align": "right", "bold": "true"}


def test_link_and_span_carry_href():
    assert L.link(LinkAttr(href="https://lpdf.io")).to_dict()["attrs"] == {"href": "https://lpdf.io"}
    assert L.span(SpanAttr(href="https://lpdf.io"), ["x"]).to_dict()["attrs"] == {"href": "https://lpdf.io"}


def test_field_carries_its_type_and_name_as_attributes():
    node = L.field(FieldAttr(type="text", name="email", max_len="40", action_url="https://lpdf.io"))
    assert node.to_dict()["attrs"] == {
        "type": "text", "name": "email", "max-len": "40", "action-url": "https://lpdf.io",
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
    doc = L.document(DocumentAttr(font="Times-Roman", debug="true"))
    assert doc.to_dict()["attrs"] == {"font": "Times-Roman", "debug": "true"}


# ── Canvas ─────────────────────────────────────────────────────────────────────

def test_rect_writes_its_attributes_as_given():
    node = L.rect(RectAttr(w="100pt", h="60pt", x="10pt", y="20pt", fill="#ff0000", radius="6pt"))
    assert node.to_dict() == {
        "type": "rect",
        "attrs": {"w": "100pt", "h": "60pt", "x": "10pt", "y": "20pt", "fill": "#ff0000", "radius": "6pt"},
    }


def test_canvas_primitives_use_their_schema_names():
    assert L.line(LineAttr(x1="0pt", y1="0pt", x2="9pt", y2="9pt", line_cap="round")).to_dict()["type"] == "line"
    assert L.circle(CircleAttr(r="5pt", cx="1pt", cy="1pt")).to_dict()["type"] == "circle"
    assert L.ellipse(EllipseAttr(rx="5pt", ry="3pt")).to_dict()["type"] == "ellipse"
    path = L.path(PathAttr(d="M 0 0 L 9 9", fill_rule="evenodd")).to_dict()
    assert path == {"type": "path", "attrs": {"d": "M 0 0 L 9 9", "fill-rule": "evenodd"}}
    assert L.img_at(CanvasImgAttr(name="logo", w="10pt", h="10pt")).to_dict()["type"] == "img"


def test_canvas_text_takes_attributes_first_and_content_second():
    node = L.text_at(
        CanvasTextAttr(x="10pt", y="20pt", font_size="12pt"),
        ["base ", L.span(SpanAttr(font="Helvetica-Bold"), ["bold"])],
    )
    d = node.to_dict()
    assert d["type"] == "text"
    assert d["attrs"] == {"x": "10pt", "y": "20pt", "font-size": "12pt"}
    assert d["nodes"][0] == "base "
    assert d["nodes"][1] == {"type": "span", "attrs": {"font": "Helvetica-Bold"}, "nodes": ["bold"]}


def test_layer_attributes_are_written_as_given():
    node = L.layer(LayerAttr(page="first", opacity="0.5", transform="rotate(45 100 100)"))
    assert node.to_dict() == {
        "type": "layer",
        "attrs": {"page": "first", "opacity": "0.5", "transform": "rotate(45 100 100)"},
        "nodes": [],
    }


def test_a_transform_is_a_string_a_layer_accepts():
    assert str(Transform.translate(10, 20)) == "matrix(1.0,0.0,0.0,1.0,10,20)"


# ── Rendering ──────────────────────────────────────────────────────────────────

def _built_document():
    return L.document(DocumentAttr(size="a4"), [
        L.section(NoAttr, [
            L.layout(NoAttr, [
                L.stack(StackAttr(gap="12pt"), [
                    L.text(TextAttr(align="right", bold="true"), ["Title"]),
                    L.text(NoAttr, ["Body ", L.span(SpanAttr(bold="true"), ["bold"]), " text"]),
                    L.link(LinkAttr(href="https://lpdf.io"), [L.text(NoAttr, ["link"])]),
                ]),
            ]),
            L.canvas(NoAttr, [
                L.layer(LayerAttr(page="each"), [
                    L.rect(RectAttr(x="40pt", y="40pt", w="100pt", h="60pt", fill="#ff0000", radius="6pt")),
                    L.text_at(CanvasTextAttr(x="40pt", y="120pt", font_size="10pt"),
                              ["Canvas ", L.span(SpanAttr(color="#0000ff"), ["text"])]),
                ]),
            ]),
        ]),
    ])


def test_a_built_document_renders_the_same_as_its_xml():
    built = _built_document()
    assert _render(built) == _render(L.to_xml(built))


def test_bold_text_is_the_bold_face_of_the_font():
    def doc(attrs: str) -> str:
        return (f'<lpdf version="1"><document><section><layout><text {attrs}>Hello</text>'
                "</layout></section></document></lpdf>")

    assert _render(doc('bold="true"')) == _render(doc('font="Helvetica-Bold"'))
    assert _render(doc('bold="true"')) != _render(doc(""))


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


def test_the_constants_are_the_schema_values():
    assert FieldType.TEXT == "text"
    assert Pin.TOP == "top"
    assert Orientation.LANDSCAPE == "landscape"
    assert BuiltinFont.TIMES_BOLD == "Times-Bold"
