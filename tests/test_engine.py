import base64
import json
from unittest.mock import patch, MagicMock

import pytest

from lpdf import PdfEngine, L, NoAttr
from lpdf.engine import EngineOptions, RenderOptions, EngineException


def _mock_subprocess_run(pdf_bytes: bytes = b"%PDF-1.4 test"):
    response = json.dumps({"pdf": base64.b64encode(pdf_bytes).decode()}).encode()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = response
    mock_result.stderr = b""
    return mock_result


def _extract_payload(mock_run) -> dict:
    call_args = mock_run.call_args
    raw = call_args.kwargs.get("input") or call_args[1]["input"]
    return json.loads(raw)


class TestRenderXml:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_render_xml_string(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("test-key")
        result = engine.render("<document><page><text>Hello</text></page></document>")

        assert result == b"%PDF-1.4 test"
        payload = _extract_payload(mock_run)
        assert payload["method"] == "render_pdf"
        assert payload["key"] == "test-key"


class TestRenderTree:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_render_tree(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        doc = L.document(NoAttr, [
            L.section(NoAttr, [L.layout(NoAttr, [L.text(NoAttr, ["Hello"])])]),
        ])
        engine = PdfEngine().set_license_key("test-key")
        result = engine.render(doc)

        assert result == b"%PDF-1.4 test"
        payload = _extract_payload(mock_run)
        assert payload["method"] == "render_tree_pdf"


class TestFontMerging:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_load_font_appears_in_payload(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.load_font("Arial", b"loaded")
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert payload["fonts"]["Arial"] == base64.b64encode(b"loaded").decode()


class TestCreatedOn:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_created_on_passthrough(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>", options=RenderOptions(created_on="2024-01-01T00:00:00Z"))

        payload = _extract_payload(mock_run)
        assert payload["created_on"] == "2024-01-01T00:00:00Z"

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_no_created_on_absent(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert "created_on" not in payload



class TestEncryption:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_encrypt_payload_sent(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.set_encryption("", "s3cr3t", {"print": False})
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert "encrypt" in payload
        assert payload["encrypt"]["user_password"] == ""
        assert payload["encrypt"]["owner_password"] == "s3cr3t"
        assert payload["encrypt"]["permissions"] == {"print": False}

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_clear_encryption_removes_payload(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.set_encryption("user", "owner")
        engine.clear_encryption()
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert "encrypt" not in payload

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_encrypt_defaults_to_empty_permissions(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.set_encryption("", "owner")
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert payload["encrypt"]["permissions"] == {}


class TestLoadImage:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_image_sent_in_payload(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("key")
        engine.load_image("logo", b"\x89PNG")
        engine.render("<doc/>")

        payload = _extract_payload(mock_run)
        assert "images" in payload
        assert payload["images"]["logo"] == base64.b64encode(b"\x89PNG").decode()


class TestAssetSrcExtraction:
    def test_xml_font_src_uses_ref_as_key(self):
        from lpdf.pdf_engine import _extract_xml_font_srcs
        xml = '<lpdf><assets><font name="body" ref="my-body" src="/fonts/MyFont.ttf"/></assets></lpdf>'
        srcs = _extract_xml_font_srcs(xml)
        assert "my-body" in srcs
        assert srcs["my-body"] == "/fonts/MyFont.ttf"
        assert "body" not in srcs

    def test_xml_font_src_falls_back_to_name(self):
        from lpdf.pdf_engine import _extract_xml_font_srcs
        xml = '<lpdf><assets><font name="body" src="/fonts/MyFont.ttf"/></assets></lpdf>'
        srcs = _extract_xml_font_srcs(xml)
        assert "body" in srcs
        assert srcs["body"] == "/fonts/MyFont.ttf"

    def test_xml_image_src_uses_ref_as_key(self):
        from lpdf.pdf_engine import _extract_xml_image_srcs
        xml = '<lpdf><assets><image name="logo" ref="my-logo" src="/img/logo.png"/></assets></lpdf>'
        srcs = _extract_xml_image_srcs(xml)
        assert "my-logo" in srcs
        assert srcs["my-logo"] == "/img/logo.png"
        assert "logo" not in srcs

    def test_xml_image_src_falls_back_to_name(self):
        from lpdf.pdf_engine import _extract_xml_image_srcs
        xml = '<lpdf><assets><image name="logo" src="/img/logo.png"/></assets></lpdf>'
        srcs = _extract_xml_image_srcs(xml)
        assert "logo" in srcs
        assert srcs["logo"] == "/img/logo.png"

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_render_xml_auto_loads_image_src(self, mock_run, tmp_path):
        mock_run.return_value = _mock_subprocess_run()
        img_file = tmp_path / "logo.png"
        img_file.write_bytes(b"\x89PNG")
        xml = f'<lpdf><assets><image name="logo" src="{img_file}"/></assets><document size="a4"><pages><page/></pages></document></lpdf>'
        engine = PdfEngine().set_license_key("key")
        engine.render(xml)
        payload = _extract_payload(mock_run)
        assert "images" in payload
        assert payload["images"]["logo"] == base64.b64encode(b"\x89PNG").decode()


class TestDataBinding:
    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_data_included_in_payload(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("test-key")
        engine.render("<lpdf/>", options=RenderOptions(data={"name": "Acme Inc"}))

        payload = _extract_payload(mock_run)
        assert "data" in payload
        assert payload["data"] == {"name": "Acme Inc"}

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_no_data_payload_has_no_data_key(self, mock_run):
        mock_run.return_value = _mock_subprocess_run()

        engine = PdfEngine().set_license_key("test-key")
        engine.render("<lpdf/>")

        payload = _extract_payload(mock_run)
        assert "data" not in payload

    @patch("lpdf.engine.wasm_runner.subprocess.run")
    def test_data_not_forwarded_for_tree_path(self, mock_run):
        """data in RenderOptions is ignored for render_tree_pdf path."""
        mock_run.return_value = _mock_subprocess_run()

        doc = L.document()
        engine = PdfEngine().set_license_key("test-key")
        engine.render(doc, options=RenderOptions(data={"name": "Acme"}))

        payload = _extract_payload(mock_run)
        assert payload["method"] == "render_tree_pdf"
        assert "data" not in payload

