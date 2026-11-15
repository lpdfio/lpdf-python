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


def test_returns_one_pdf_with_the_pages_of_the_sources_in_order() -> None:
    output = PdfEngine().merge([MergeSource(name="a.pdf", pdf=_pdf(2)), MergeSource(name="b.pdf", pdf=_pdf(1))])
    assert output.startswith(b"%PDF-")
    assert _page_count(output) == 3


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
