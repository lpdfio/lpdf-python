import base64
import json
from unittest.mock import patch

import pytest

from lpdf import PdfEngine, L, NoAttr, DocumentAttr, DocumentMeta, DocumentOutput, Cipher, Permission
from lpdf.engine import EngineOptions, RenderOptions, EngineException


def _engine_response(pdf_bytes: bytes = b"%PDF-1.4 test") -> dict:
    return {"pdf": base64.b64encode(pdf_bytes).decode()}


def _extract_payload(invoke) -> dict:
    """The request the engine was sent, by the stand-in for ``WasmRunner.invoke``."""
    return invoke.call_args.args[0]


class TestRenderXml:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_render_xml_string(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("test-key")
        result = engine.render("<document><page><text>Hello</text></page></document>")

        assert result == b"%PDF-1.4 test"
        payload = _extract_payload(invoke)
        assert payload["method"] == "render_pdf"
        assert payload["key"] == "test-key"


class TestRenderTree:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_render_tree(self, invoke):
        invoke.return_value = _engine_response()

        doc = L.document(NoAttr, [
            L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])]),
        ])
        engine = PdfEngine().set_license_key("test-key")
        result = engine.render(doc)

        assert result == b"%PDF-1.4 test"
        payload = _extract_payload(invoke)
        assert payload["method"] == "render_tree_pdf"


class TestFontMerging:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_load_font_appears_in_payload(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.load_font("Arial", b"loaded")
        engine.render("<doc/>")

        payload = _extract_payload(invoke)
        assert payload["fonts"]["Arial"] == base64.b64encode(b"loaded").decode()


class TestCreatedOn:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_created_on_passthrough(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", options=RenderOptions(created_on="2024-01-01T00:00:00Z"))

        payload = _extract_payload(invoke)
        assert payload["created_on"] == "2024-01-01T00:00:00Z"

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_no_created_on_absent(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>")

        payload = _extract_payload(invoke)
        assert "created_on" not in payload



class TestEncryption:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_the_passwords_go_with_the_render(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", RenderOptions(user_password="", owner_password="s3cr3t"))

        payload = _extract_payload(invoke)
        assert payload["user_password"] == ""
        assert payload["owner_password"] == "s3cr3t"
        assert "encrypt" not in payload
        assert "skip_encryption" not in payload

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_a_render_without_passwords_sends_none(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>")

        payload = _extract_payload(invoke)
        assert not {"user_password", "owner_password", "entropy", "skip_encryption"} & payload.keys()

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_a_password_sends_32_bytes_of_entropy(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", RenderOptions(owner_password="owner"))

        assert len(base64.b64decode(_extract_payload(invoke)["entropy"])) == 32

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_every_render_gets_fresh_entropy(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", RenderOptions(owner_password="owner"))
        first = _extract_payload(invoke)["entropy"]
        engine.render("<doc/>", RenderOptions(owner_password="owner"))
        second = _extract_payload(invoke)["entropy"]

        assert first != second

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_skip_encryption_is_sent_by_name(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", RenderOptions(skip_encryption=True))

        payload = _extract_payload(invoke)
        assert payload["skip_encryption"] is True
        assert "entropy" not in payload

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_passwords_with_skip_encryption_are_left_for_the_engine_to_refuse(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", RenderOptions(owner_password="owner", skip_encryption=True))

        payload = _extract_payload(invoke)
        assert payload["owner_password"] == "owner"
        assert payload["skip_encryption"] is True

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_the_output_of_a_kit_document_goes_in_its_attrs(self, invoke):
        invoke.return_value = _engine_response()

        document = L.document(
            DocumentAttr(output=DocumentOutput(encrypt=Cipher.AES_256, allow=f"{Permission.PRINT} {Permission.FILL_FORMS}")),
            [L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])])],
        )
        PdfEngine().set_license_key("key").render(document, RenderOptions(owner_password="owner"))

        tree = json.loads(_extract_payload(invoke)["input"])
        assert tree["attrs"]["output"] == {"encrypt": "aes-256", "allow": "print fill-forms"}

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_linearize_of_a_kit_document_goes_in_its_output_as_a_boolean(self, invoke):
        invoke.return_value = _engine_response()

        document = L.document(
            DocumentAttr(output=DocumentOutput(encrypt=Cipher.AES_256, linearize=True)),
            [L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])])],
        )
        PdfEngine().set_license_key("key").render(document, RenderOptions(owner_password="owner"))

        tree = json.loads(_extract_payload(invoke)["input"])
        assert tree["attrs"]["output"] == {"encrypt": "aes-256", "linearize": True}


    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_pdfa_of_a_kit_document_goes_in_its_output_with_the_date(self, invoke):
        invoke.return_value = _engine_response()

        document = L.document(
            DocumentAttr(output=DocumentOutput(pdfa="2u")),
            [L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])])],
        )
        PdfEngine().set_license_key("key").render(document, RenderOptions(created_on="2026-10-31T09:30:00Z"))

        payload = _extract_payload(invoke)
        assert json.loads(payload["input"])["attrs"]["output"] == {"pdfa": "2u"}
        assert payload["created_on"] == "2026-10-31T09:30:00Z"

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_pdfua_and_lang_of_a_kit_document_go_in_its_output_and_meta(self, invoke):
        invoke.return_value = _engine_response()

        document = L.document(
            DocumentAttr(meta=DocumentMeta(title="Report", lang="en-US"), output=DocumentOutput(pdfua="1")),
            [L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])])],
        )
        PdfEngine().set_license_key("key").render(document, RenderOptions(created_on="2026-10-31"))

        attrs = json.loads(_extract_payload(invoke)["input"])["attrs"]
        assert attrs["output"] == {"pdfua": "1"}
        assert attrs["meta"] == {"title": "Report", "lang": "en-US"}


class TestLoadImage:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_image_sent_in_payload(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("key")
        engine.load_image("logo", b"\x89PNG")
        engine.render("<doc/>")

        payload = _extract_payload(invoke)
        assert "images" in payload
        assert payload["images"]["logo"] == base64.b64encode(b"\x89PNG").decode()


class TestAssetSrcExtraction:
    def test_xml_font_src_uses_ref_as_key(self):
        from lpdf.pdf_engine import _parse_xml, _xml_srcs
        xml = '<lpdf><assets><font name="body" ref="my-body" src="/fonts/MyFont.ttf"/></assets></lpdf>'
        srcs = _xml_srcs(_parse_xml(xml), ".//assets/font")
        assert "my-body" in srcs
        assert srcs["my-body"] == "/fonts/MyFont.ttf"
        assert "body" not in srcs

    def test_xml_font_src_falls_back_to_name(self):
        from lpdf.pdf_engine import _parse_xml, _xml_srcs
        xml = '<lpdf><assets><font name="body" src="/fonts/MyFont.ttf"/></assets></lpdf>'
        srcs = _xml_srcs(_parse_xml(xml), ".//assets/font")
        assert "body" in srcs
        assert srcs["body"] == "/fonts/MyFont.ttf"

    def test_xml_image_src_uses_ref_as_key(self):
        from lpdf.pdf_engine import _parse_xml, _xml_srcs
        xml = '<lpdf><assets><image name="logo" ref="my-logo" src="/img/logo.png"/></assets></lpdf>'
        srcs = _xml_srcs(_parse_xml(xml), ".//assets/image")
        assert "my-logo" in srcs
        assert srcs["my-logo"] == "/img/logo.png"
        assert "logo" not in srcs

    def test_xml_image_src_falls_back_to_name(self):
        from lpdf.pdf_engine import _parse_xml, _xml_srcs
        xml = '<lpdf><assets><image name="logo" src="/img/logo.png"/></assets></lpdf>'
        srcs = _xml_srcs(_parse_xml(xml), ".//assets/image")
        assert "logo" in srcs
        assert srcs["logo"] == "/img/logo.png"

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_render_xml_auto_loads_image_src(self, invoke, tmp_path):
        invoke.return_value = _engine_response()
        img_file = tmp_path / "logo.png"
        img_file.write_bytes(b"\x89PNG")
        xml = f'<lpdf><assets><image name="logo" src="{img_file}"/></assets><document size="a4"><pages><page/></pages></document></lpdf>'
        engine = PdfEngine().set_license_key("key")
        engine.render(xml)
        payload = _extract_payload(invoke)
        assert "images" in payload
        assert payload["images"]["logo"] == base64.b64encode(b"\x89PNG").decode()


class TestDataBinding:
    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_data_included_in_payload(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("test-key")
        engine.render("<lpdf/>", options=RenderOptions(data={"name": "Acme Inc"}))

        payload = _extract_payload(invoke)
        assert "data" in payload
        assert payload["data"] == {"name": "Acme Inc"}

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_no_data_payload_has_no_data_key(self, invoke):
        invoke.return_value = _engine_response()

        engine = PdfEngine().set_license_key("test-key")
        engine.render("<lpdf/>")

        payload = _extract_payload(invoke)
        assert "data" not in payload

    @patch("lpdf.engine.wasm_runner.WasmRunner.invoke")
    def test_data_not_forwarded_for_tree_path(self, invoke):
        """data in RenderOptions is ignored for render_tree_pdf path."""
        invoke.return_value = _engine_response()

        doc = L.document()
        engine = PdfEngine().set_license_key("test-key")
        engine.render(doc, options=RenderOptions(data={"name": "Acme"}))

        payload = _extract_payload(invoke)
        assert payload["method"] == "render_tree_pdf"
        assert "data" not in payload

