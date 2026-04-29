import pytest

from lpdf import PdfEngine

from .snapshot_helper import EXAMPLES, FIXTURES, HAS_FIXTURES, compare_or_update

pytestmark = pytest.mark.skipif(
    not HAS_FIXTURES,
    reason="fixture files not available outside the monorepo",
)


@pytest.mark.parametrize("name", EXAMPLES)
def test_fixture_matches_stored_hash(name: str) -> None:
    xml = (FIXTURES / f"{name}.xml").read_text(encoding="utf-8")
    engine = PdfEngine().set_license_key("test-key")
    pdf_bytes = engine.render(xml)
    compare_or_update(name, pdf_bytes)


def test_output_is_pdf() -> None:
    xml = (FIXTURES / "example1.xml").read_text(encoding="utf-8")
    pdf_bytes = PdfEngine().set_license_key("test-key").render(xml)
    assert pdf_bytes[:5] == b"%PDF-"


def test_custom_font_does_not_throw() -> None:
    xml = (FIXTURES / "example1.xml").read_text(encoding="utf-8")
    engine = PdfEngine().set_license_key("test-key")
    engine.load_font("TestFont", b"")
    pdf_bytes = engine.render(xml)
    assert pdf_bytes[:5] == b"%PDF-"
