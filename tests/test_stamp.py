"""Stamps: PNG images drawn over the pages of an existing PDF, through the engine's ``stamp`` request."""

import re
import struct
import zlib

import pytest

from lpdf import L, PdfEngine, StampAttr
from lpdf.engine import EngineException


def _chunk(tag: bytes, data: bytes) -> bytes:
    # The decoder doesn't check the CRC, which is left 0.
    return struct.pack(">I", len(data)) + tag + data + b"\0\0\0\0"


def _png(width: int, height: int) -> bytes:
    """An RGB PNG of ``width`` by ``height`` pixels, all red."""
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    rows = b"".join(b"\0" + bytes([200, 40, 40]) * width for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(rows)) + _chunk(b"IEND", b"")


def _pdf(pages: int = 2) -> bytes:
    """A PDF of ``pages`` pages, rendered by the engine."""
    sections = "".join(f"<section><layout><text>Page {i}</text></layout></section>" for i in range(1, pages + 1))
    return PdfEngine().render(f'<lpdf version="1"><document>{sections}</document></lpdf>')


def _update(pdf: bytes, out: bytes) -> str:
    """The text of what a stamp appended to ``pdf``."""
    return out[len(pdf):].decode("latin-1")


def test_a_stamp_returns_the_input_with_an_update_after_it_that_draws_the_image() -> None:
    pdf = _pdf()
    out = L.engine().stamp(pdf, [
        StampAttr(image=_png(60, 30), page="last", x="72pt", y="72pt", width="144pt", height="36pt", justify="end"),
    ])
    assert len(out) > len(pdf) and out.startswith(pdf)
    assert "/LpdfStamp0 Do" in _update(pdf, out)


def test_an_image_given_to_several_stamps_is_embedded_once() -> None:
    pdf = _pdf(3)
    seal = _png(40, 40)
    out = PdfEngine().stamp(pdf, [
        StampAttr(image=seal, page="each", anchor="top-right", x="-36pt", y="36pt", width="40pt", height="40pt"),
        StampAttr(image=seal, page="1", anchor="center", width="40pt", height="40pt", max_grow=2),
        StampAttr(image=_png(20, 10), page="2-3", x="1in", y="1in", width="1in", height="1in"),
    ])
    assert len(re.findall(r"/Subtype\s*/Image", _update(pdf, out))) == 2


def test_without_a_license_key_each_stamp_gets_the_attribution_line_linked_to_lpdf_io() -> None:
    pdf = _pdf(1)
    out = PdfEngine().stamp(pdf, [StampAttr(image=_png(10, 10), page="1", anchor="center", width="50pt", height="50pt")])
    assert "(https://lpdf.io)" in _update(pdf, out)


def test_a_page_the_pdf_does_not_have_and_an_image_that_is_not_a_png_are_engine_errors() -> None:
    pdf = _pdf(2)
    engine = PdfEngine()
    with pytest.raises(EngineException, match="stamp 1: the PDF has no page 3: it has 2 pages"):
        engine.stamp(pdf, [StampAttr(image=_png(10, 10), page="3", x="0pt", y="0pt", width="10pt", height="10pt")])
    with pytest.raises(EngineException, match="the image is a JPEG, and a stamp takes a PNG"):
        engine.stamp(pdf, [StampAttr(image=b"\xff\xd8\xff\xe0\0\0", page="1", x="0pt", y="0pt", width="10pt", height="10pt")])
    with pytest.raises(EngineException, match="has no position: give it x and y, or an anchor"):
        engine.stamp(pdf, [StampAttr(image=_png(10, 10), page="1", width="10pt", height="10pt")])


def test_an_image_that_is_not_bytes_is_a_type_error() -> None:
    with pytest.raises(TypeError, match="stamp 1: image must be the PNG's bytes"):
        PdfEngine().stamp(b"", [StampAttr(image="seal.png", page="1", x="0pt", y="0pt", width="1pt", height="1pt")])
