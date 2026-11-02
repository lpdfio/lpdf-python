"""Big documents, the memory cap of a render, how deep a document may nest, and an engine that crashes."""

import json
import re
from pathlib import Path

import pytest
import wasmtime

from lpdf import EngineException, EngineOptions, L, PdfEngine, RenderOptions

from .snapshot_helper import FIXTURES, HAS_FIXTURES, compare_or_update

needs_fixtures = pytest.mark.skipif(not HAS_FIXTURES, reason="fixture files not available outside the monorepo")

CAP_ERROR = "the render needs more memory than its cap of "
DEPTH_ERROR = "is nested 101 levels deep, past the limit of 100"
ENGINE_CRASHED = (
    "The engine crashed during the render. This is a bug in Lpdf, or the render ran out of memory before its cap "
    "stopped it: please report it with the document at https://github.com/lpdfio/lpdf/issues."
)


def _fixture(name: str) -> str:
    return (FIXTURES / f"{name}.xml").read_text(encoding="utf-8")


def _bench_max_copied(copies: int) -> str:
    """``bench_max.xml`` with its sections copied: 188 pages and 1 MB of XML for each copy."""
    xml = _fixture("bench_max")
    start = xml.index("<section")
    end = xml.rindex("</section>") + len("</section>")
    return xml[:start] + xml[start:end] * copies + xml[end:]


def _page_count(pdf: bytes) -> int:
    """The number of pages of a PDF: its page objects, which the engine writes uncompressed."""
    return len(re.findall(rb"/Type /Page\b(?!s)", pdf))


def _nested_xml(depth: int) -> str:
    """A document whose columns nest so that its deepest element is ``depth`` levels deep, ``<lpdf>`` included."""
    # <lpdf>, <document>, <section>, <layout> and the <text> in the deepest column.
    columns = depth - 5
    return (
        '<lpdf version="1"><document><section><layout>' + "<column>" * columns + "<text>deep</text>"
        + "</column>" * columns + "</layout></section></document></lpdf>"
    )


def _nested_tree(depth: int):
    """The tree of ``_nested_xml(depth)``."""
    node = L.text(None, ["deep"])
    for _ in range(depth - 5):
        node = L.column(None, [node])
    return L.document(None, [L.section(None, [L.layout(None, [node])])])


@needs_fixtures
def test_bench_max_copied_16_times_renders_its_3008_pages() -> None:
    xml = _bench_max_copied(16)
    assert len(xml) > 16_000_000

    pdf = PdfEngine(EngineOptions(timeout=0)).render(xml)

    assert _page_count(pdf) == 3008


def test_a_document_tree_whose_json_is_over_4_mb_renders() -> None:
    line = "A paragraph of a long report, with enough words in it to fill a line or two of the page. " * 2
    sections = [
        L.section(None, [L.layout(None, [L.text(None, [f"{s}.{i} {line}"]) for i in range(20)])])
        for s in range(1200)
    ]
    tree = L.document(None, sections)
    assert len(json.dumps(tree.to_dict())) > 4 * 1_048_576

    pdf = PdfEngine(EngineOptions(timeout=0)).render(tree)

    assert _page_count(pdf) >= 1200


@needs_fixtures
def test_a_render_past_the_cap_stops_with_its_error_and_the_next_renders_right() -> None:
    engine = PdfEngine(EngineOptions(max_memory_mb=8)).set_license_key("test-key")

    with pytest.raises(EngineException, match=re.escape(CAP_ERROR + "8 MB")):
        engine.render(_fixture("bench_max"))

    compare_or_update("bench_m", engine.render(_fixture("bench_m"), RenderOptions(skip_encryption=True)))


@needs_fixtures
def test_the_same_document_renders_under_a_higher_cap() -> None:
    assert _page_count(PdfEngine(EngineOptions(max_memory_mb=64)).render(_fixture("bench_max"))) == 188


def test_a_big_data_object_counts_toward_the_cap() -> None:
    xml = '<lpdf version="1"><document><section><layout><text data-value="title">x</text></layout></section></document></lpdf>'
    rows = [{"name": f"Row {i}", "note": "Some text that is bound"} for i in range(200_000)]
    data = {"title": "Report", "rows": rows}

    with pytest.raises(EngineException, match=re.escape(CAP_ERROR + "8 MB")):
        PdfEngine(EngineOptions(max_memory_mb=8)).render(xml, RenderOptions(data=data))
    pdf = PdfEngine(EngineOptions(max_memory_mb=256)).render(xml, RenderOptions(data=data))
    assert _page_count(pdf) == 1


@pytest.mark.parametrize("megabytes", [0, -1, 4097, 1.5, True])
def test_a_cap_that_is_not_a_whole_number_from_1_to_4096_is_refused(megabytes: object) -> None:
    with pytest.raises(ValueError, match=f"max_memory_mb must be a whole number of megabytes from 1 to 4096, not {megabytes}"):
        EngineOptions(max_memory_mb=megabytes)  # type: ignore[arg-type]  # the wrong types are the point


def test_a_document_nested_100_levels_deep_renders_as_xml_and_as_a_tree() -> None:
    engine = PdfEngine()

    assert _page_count(engine.render(_nested_xml(100))) == 1
    assert _page_count(engine.render(_nested_tree(100))) == 1


def test_a_document_nested_101_levels_deep_fails_with_the_depth_error_as_xml_and_as_a_tree() -> None:
    engine = PdfEngine()

    with pytest.raises(EngineException, match=re.escape("<text> at line 1")) as xml:
        engine.render(_nested_xml(101))
    with pytest.raises(EngineException, match=re.escape("the node 'text'")) as tree:
        engine.render(_nested_tree(101))

    assert DEPTH_ERROR in str(xml.value)
    assert DEPTH_ERROR in str(tree.value)


@pytest.mark.parametrize("wat, code", [
    ('(module (func (export "_start") unreachable))', wasmtime.TrapCode.UNREACHABLE),
    ('(module (func $down (call $down)) (func (export "_start") (call $down)))', wasmtime.TrapCode.STACK_OVERFLOW),
])
def test_a_crash_raises_the_crash_message_from_the_trap(tmp_path: Path, wat: str, code: wasmtime.TrapCode) -> None:
    binary = tmp_path / "engine.wasm"
    binary.write_bytes(wasmtime.wat2wasm(wat))

    with pytest.raises(EngineException) as crashed:
        PdfEngine(EngineOptions(wasm_binary=str(binary))).render(_nested_xml(10))

    assert str(crashed.value) == ENGINE_CRASHED
    assert isinstance(crashed.value.__cause__, wasmtime.Trap)
    assert crashed.value.__cause__.trap_code == code
