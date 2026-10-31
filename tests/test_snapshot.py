import pytest

from lpdf import PdfEngine, RenderOptions
from lpdf.engine import EngineException

from .snapshot_helper import EXAMPLES, FIXTURES, HAS_FIXTURES, compare_or_update

pytestmark = pytest.mark.skipif(
    not HAS_FIXTURES,
    reason="fixture files not available outside the monorepo",
)


@pytest.mark.parametrize("name", EXAMPLES)
def test_fixture_matches_stored_hash(name: str) -> None:
    xml = (FIXTURES / f"{name}.xml").read_text(encoding="utf-8")
    engine = PdfEngine().set_license_key("test-key")
    # showcase-encryption asks for encryption in its output: its snapshot is the file unencrypted.
    pdf_bytes = engine.render(xml, RenderOptions(skip_encryption=True))
    compare_or_update(name, pdf_bytes)


def test_output_is_pdf() -> None:
    xml = (FIXTURES / "example1.xml").read_text(encoding="utf-8")
    pdf_bytes = PdfEngine().set_license_key("test-key").render(xml)
    assert pdf_bytes[:5] == b"%PDF-"


def _pdfa_xml(level: str = "2b", body: str = '<column background="#e8f0fc" height="40pt"/>') -> str:
    """A document with no text of its own that asks for PDF/A: the attribution line's name, in its embedded face, is
    its one text."""
    return f'<lpdf version="1"><document><output pdfa="{level}"/><section><layout>{body}</layout></section></document></lpdf>'


def test_writes_pdfa_when_the_output_asks_for_it_dated_by_created_on() -> None:
    engine = PdfEngine().set_license_key("test-key")
    pdf_bytes = engine.render(_pdfa_xml("2u"), RenderOptions(created_on="2026-10-31T09:30:00Z"))
    assert b"<pdfaid:conformance>U</pdfaid:conformance>" in pdf_bytes
    assert b"/S /GTS_PDFA1" in pdf_bytes
    assert b"/ModDate (D:20261031093000Z)" in pdf_bytes


def test_refuses_pdfa_without_created_on_and_text_in_a_built_in_font() -> None:
    engine = PdfEngine().set_license_key("test-key")
    with pytest.raises(EngineException, match="created_on"):
        engine.render(_pdfa_xml())
    with pytest.raises(EngineException, match='"Hello" is in Helvetica'):
        engine.render(_pdfa_xml("2b", "<text>Hello</text>"), RenderOptions(created_on="2026-10-31"))


def test_custom_font_does_not_throw() -> None:
    xml = (FIXTURES / "example1.xml").read_text(encoding="utf-8")
    engine = PdfEngine().set_license_key("test-key")
    engine.load_font("TestFont", b"")
    pdf_bytes = engine.render(xml)
    assert pdf_bytes[:5] == b"%PDF-"
