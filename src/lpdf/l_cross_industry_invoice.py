from __future__ import annotations

import base64
from typing import Any

from .engine.engine_exception import EngineException
from .engine.invoice_format import InvoiceFormat
from .engine.wasm_runner import WasmRunner
from .kit.document import PdfDocument
from .pdf_engine import PdfEngine, default_wasm_binary


def _bytes_of(name: str, xml: Any) -> bytes:
    """The bytes of an XML given as text or bytes."""
    if isinstance(xml, str):
        return xml.encode("utf-8")
    if isinstance(xml, (bytes, bytearray, memoryview)):
        return bytes(xml)
    raise TypeError(f"{name} must be the XML as a str or its bytes, not {type(xml).__name__}")


def _map_of(invoice_map: Any) -> str | None:
    """The text of a map given as text or bytes, or None for the default."""
    if invoice_map is None:
        return None
    return invoice_map if isinstance(invoice_map, str) else _bytes_of("invoice_map", invoice_map).decode("utf-8")


def _reader() -> WasmRunner:
    """The engine that reads invoices with no engine of the caller's: it uses no fonts and no key, under the default
    time and memory limits."""
    return WasmRunner(wasm_binary=default_wasm_binary())


def _read(runner: WasmRunner, invoice_xml: bytes, invoice_map: str | None, format: InvoiceFormat | None) -> dict:
    """The values of an invoice, read by ``runner``, with the format function of each typed one applied."""
    if format is not None and not isinstance(format, InvoiceFormat):
        raise TypeError("format must be an InvoiceFormat")
    answer = runner.invoke({
        "method": "extract_invoice_data",
        "invoice_xml": base64.b64encode(invoice_xml).decode(),
        "invoice_map": invoice_map,
    })
    data = answer["data"]
    for typed in answer["typed"]:
        fn = getattr(format, typed["type"], None) if format is not None else None
        if fn is None:
            continue
        *path, last = typed["at"]
        holder = data
        for step in path:
            holder = holder[step]
        text = fn(holder[last], typed["name"])
        # Text only: str() would bind the word "None", which a dict's get() gives for a code it has no word for, or a
        # number written as Python writes it rather than as the caller chose.
        if not isinstance(text, str):
            returned = "None" if text is None else type(text).__name__
            raise TypeError(
                f"format.{typed['type']} returned {returned} for '{typed['name']}': return the text to bind, or the "
                "value as it came."
            )
        holder[last] = text
    return data


class LCrossIndustryInvoice:
    """A Factur-X / ZUGFeRD invoice PDF made from the invoice's XML, the EN 16931 Cross Industry Invoice that accounting
    software writes. The engine reads the XML through a map and checks it; this class hands the values to the caller's
    ``InvoiceFormat`` functions.

    ::

        pdf = LCrossIndustryInvoice.generate_pdf(L.engine(), template,
            invoice_xml=Path("invoice.xml").read_bytes(),
            format=InvoiceFormat(date=lambda value, _: date.fromisoformat(value).strftime("%d.%m.%Y")),
            created_on=datetime.now(timezone.utc).isoformat())
    """

    @staticmethod
    def generate_pdf(
        engine: PdfEngine,
        template_or_document: str | PdfDocument,
        *,
        invoice_xml: str | bytes,
        invoice_map: str | bytes | None = None,
        format: InvoiceFormat | None = None,
        data: dict | None = None,
        created_on: str,
    ) -> bytes:
        """The invoice's PDF, a Factur-X / ZUGFeRD file: a template, an XML string, filled with the values of the
        invoice, which it binds under the map's prefix (``invoice:seller.name``) beside ``data``, or a document built
        in code, which has no bindings. The file is PDF/A-3, 3b unless the document sets 3a or 3u, and carries the XML
        as ``factur-x.xml``, or ``xrechnung.xml`` for XRECHNUNG. The document says only how the invoice looks: it
        declares no invoice file.

        The engine carries the fonts, the license key and the limits, its timeout and ``max_memory_mb``, under which it
        reads the invoice for a template and renders the file. ``invoice_map`` is the map, an XML document, or Lpdf's
        default map without it. ``created_on`` is the ISO 8601 creation date of the file, which PDF/A requires.

        :raises EngineException: for what ``extract_invoice_data`` refuses, a template path under the prefix that the
            map lacks, a PDF/A level other than 3a, 3b or 3u, ``encrypt``, ``pdfx``, and a document that declares the
            invoice file; or when the read or the render runs past the engine's timeout or needs more than its
            ``max_memory_mb``.
        :raises TypeError: when the XML or the map is not text or bytes, ``format`` is not an ``InvoiceFormat``, or one
            of its functions returns anything but a ``str``.
        """
        xml = _bytes_of("invoice_xml", invoice_xml)
        if not isinstance(created_on, str):
            raise TypeError("generate_pdf needs created_on, which PDF/A requires")
        invoice: dict = {"xml": base64.b64encode(xml).decode()}
        if not isinstance(template_or_document, PdfDocument):
            invoice_map_text = _map_of(invoice_map)
            invoice["map"] = invoice_map_text
            invoice["data"] = _read(engine._runner(), xml, invoice_map_text, format)
        return engine._render(template_or_document, created_on=created_on, data=data, invoice=invoice)

    @staticmethod
    def extract_invoice_data(
        invoice_xml: str | bytes,
        *,
        invoice_map: str | bytes | None = None,
        format: InvoiceFormat | None = None,
    ) -> dict:
        """The values of an invoice as plain data: a value is a field, a group a dict, a list a list, all text, as the
        map names them. A value the invoice lacks is absent, and a list with no items is empty. For code that needs the
        values itself: a document built in code, choosing a template, naming the file.

        It uses no engine: it reads no fonts and no key, under the default time and memory limits.

        :raises EngineException: when the map is not one or doesn't fit the schema, the invoice is not a Cross Industry
            Invoice or is MINIMUM or BASIC WL, or lacks a value the map marks required.
        :raises TypeError: when the XML or the map is not text or bytes, ``format`` is not an ``InvoiceFormat``, or one
            of its functions returns anything but a ``str``.
        """
        return _read(_reader(), _bytes_of("invoice_xml", invoice_xml), _map_of(invoice_map), format)

    @staticmethod
    def default_invoice_map() -> str:
        """Lpdf's default invoice map, as XML text: the values EN 16931 numbers but the parties' identifiers BT-29,
        BT-46, BT-60 and BT-71, what a line may hold several of, and an attached file's content. The start of a map
        of your own."""
        answer = _reader().invoke({"method": "default_invoice_map"})
        if "map" not in answer:
            raise EngineException("Unexpected response from the engine.")
        return answer["map"]
