"""Merge: existing PDFs drawn into one PDF made for printing, through the engine's ``merge`` request."""

import re

import pytest

from lpdf import EngineException, MergeOptions, MergeSource, PdfEngine, RenderOptions

# What the SDK puts before the engine's message in an EngineException.
_PREFIX = "lpdf render error: "


def _pdf(pages: int = 1, output: str = "", options: RenderOptions | None = None) -> bytes:
    """A PDF of ``pages`` pages, rendered by the engine, with an owner password and ``output`` when it has them."""
    sections = "".join(f"<section><layout><text>Page {i}</text></layout></section>" for i in range(1, pages + 1))
    return PdfEngine().render(f'<lpdf version="1"><document>{output}{sections}</document></lpdf>', options)


def _page_count(output: bytes) -> int:
    """How many pages a merged PDF has: its page objects, which the merge writes uncompressed."""
    return len(re.findall(r"/Type\s*/Page(?![s\w])", output.decode("latin-1")))


def _message(error: pytest.ExceptionInfo[EngineException]) -> str:
    """The engine's message of an error, as the engine wrote it."""
    return str(error.value).removeprefix(_PREFIX)


def _signed_pdf() -> bytes:
    """A PDF of one empty page whose catalog holds a certifying signature, which is what makes a file signed."""
    objects = [
        "<< /Type /Catalog /Pages 2 0 R /Perms << /DocMDP 4 0 R >> >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >>",
        "<< /Type /Sig /Filter /Adobe.PPKLite /SubFilter /adbe.pkcs7.detached >>",
    ]
    pdf = "%PDF-1.7\n"
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{number} 0 obj\n{body}\nendobj\n"
    xref = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    pdf += "".join(f"{offset:010d} 00000 n \n" for offset in offsets)
    pdf += f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return pdf.encode("latin-1")


def test_returns_one_pdf_with_the_pages_of_the_sources() -> None:
    output = PdfEngine().merge([MergeSource(name="a.pdf", pdf=_pdf(2)), MergeSource(name="b.pdf", pdf=_pdf(1))])
    assert output.startswith(b"%PDF-")
    assert _page_count(output) == 3


def test_puts_the_pages_in_the_order_of_the_sources() -> None:
    # With double_sided a blank side follows a document of odd length unless it is the last: the order decides how many.
    odd, even = MergeSource(name="odd.pdf", pdf=_pdf(1)), MergeSource(name="even.pdf", pdf=_pdf(2))
    engine = PdfEngine()
    assert _page_count(engine.merge([odd, even], MergeOptions(double_sided=True))) == 4
    assert _page_count(engine.merge([even, odd], MergeOptions(double_sided=True))) == 3


def test_adds_a_blank_side_after_a_document_with_an_odd_number_of_pages_with_double_sided_and_none_after_the_last() -> None:
    odd, even = _pdf(1), _pdf(2)
    sources = [
        MergeSource(name="odd.pdf", pdf=odd),
        MergeSource(name="even.pdf", pdf=even),
        MergeSource(name="odd-again.pdf", pdf=odd),
    ]
    engine = PdfEngine()
    assert _page_count(engine.merge(sources)) == 4
    assert _page_count(engine.merge(sources, MergeOptions(double_sided=True))) == 5


def test_raises_an_error_that_names_the_file_that_is_not_a_pdf() -> None:
    with pytest.raises(EngineException) as error:
        PdfEngine().merge([MergeSource(name="a.pdf", pdf=_pdf()), MergeSource(name="notes.txt", pdf=b"hello")])
    assert _message(error) == "notes.txt: the file is not a PDF: it doesn't start with %PDF-"


def test_refuses_a_file_whose_owner_restricts_printing_or_copying_unless_allow_restricted_is_set() -> None:
    limited = _pdf(1, '<output encrypt="aes-256" allow="print"/>', RenderOptions(owner_password="owner"))
    engine = PdfEngine()
    with pytest.raises(EngineException) as error:
        engine.merge([MergeSource(name="limited.pdf", pdf=limited)])
    assert _message(error) == (
        "limited.pdf: the owner restricts printing or copying: set the allow-restricted option to merge it anyway"
    )
    output = engine.merge([MergeSource(name="limited.pdf", pdf=limited)], MergeOptions(allow_restricted=True))
    assert _page_count(output) == 1
    assert "/Encrypt" not in output.decode("latin-1")


def test_refuses_a_signed_file_unless_allow_signed_is_set() -> None:
    signed = [MergeSource(name="signed.pdf", pdf=_signed_pdf())]
    engine = PdfEngine()
    with pytest.raises(EngineException) as error:
        engine.merge(signed)
    assert _message(error).startswith("signed.pdf: the file is signed")
    assert "set the allow-signed option" in _message(error)
    assert _page_count(engine.merge(signed, MergeOptions(allow_signed=True))) == 1


def test_raises_an_error_for_an_empty_list() -> None:
    with pytest.raises(EngineException) as error:
        PdfEngine().merge([])
    assert _message(error) == "no PDFs were given: give merge at least one"


def test_a_source_that_is_not_a_name_and_bytes_is_a_type_error() -> None:
    engine = PdfEngine()
    with pytest.raises(TypeError, match=r"source 1 \(a\.pdf\): pdf must be the PDF's bytes"):
        engine.merge([MergeSource(name="a.pdf", pdf="bytes")])  # type: ignore[arg-type]  # the wrong type is the test
    with pytest.raises(TypeError, match="source 1: must be a MergeSource with a name"):
        engine.merge([{"name": "a.pdf", "pdf": _pdf()}])  # type: ignore[list-item]  # the wrong type is the test
