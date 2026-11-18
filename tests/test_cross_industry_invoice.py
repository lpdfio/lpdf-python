"""LCrossIndustryInvoice: a Factur-X / ZUGFeRD invoice PDF made from the invoice's XML.

The template is core's showcase-cross-industry-invoice fixture. It, the invoices, the font and the snapshot hash come
from core's test/fixtures, test/assets and test/snapshots, which CI copies in from the core tag.
"""

import json
from datetime import date
from decimal import Decimal

import pytest

from lpdf import (
    ColumnAttr, DividerAttr, DocumentAssets, DocumentAttr, DocumentMeta, EngineException, FontAttr, InvoiceFormat, L,
    LCrossIndustryInvoice, LayoutAttr, NoAttr, RowAttr, TableAttr, TextAttr,
)

from .snapshot_helper import FIXTURES, HAS_FIXTURES, ROOT, compare_or_update

needs_fixtures = pytest.mark.skipif(not HAS_FIXTURES, reason="fixture files not available outside the monorepo")

FACTURX = ROOT / "test" / "assets" / "files" / "facturx"
CREATED_ON = "2026-11-18T10:00:00Z"
NOTE = "Payable within 30 days, by bank transfer."


def invoice(name: str) -> bytes:
    return (FACTURX / name).read_bytes()


def template() -> str:
    return (FIXTURES / "showcase-cross-industry-invoice.xml").read_text(encoding="utf-8")


def engine():
    """An unlicensed engine with the templates' font loaded under its name, ``body``."""
    font = (ROOT / "test" / "assets" / "fonts" / "SourceSans3-Regular.otf").read_bytes()
    return L.engine().load_font("body", font)


CODE_NAMES = {
    "typeCode": {"380": "Invoice", "381": "Credit note"},
    "lines.unit": {"H87": "pcs", "KGM": "kg"},
}

# A date as "31 October 2026", an amount with a comma between thousands and two decimals, and a code as its word in
# CODE_NAMES for its entry, or as the invoice writes it when the entry has no word for it.
FORMAT = InvoiceFormat(
    date=lambda value, _: f"{date.fromisoformat(value).day} {date.fromisoformat(value):%B %Y}",
    amount=lambda value, _: f"{Decimal(value):,.2f}",
    code=lambda value, entry_name: CODE_NAMES.get(entry_name, {}).get(value, value),
)


def document_in_code(invoice_data: dict):
    """The page of core's ``showcase-cross-industry-invoice`` fixture, built in code with the values of
    ``extract_invoice_data``."""
    muted = TextAttr(font_size="9pt", color="#5b6475")
    muted_right = TextAttr(font_size="9pt", color="#5b6475", align="right")
    right = TextAttr(align="right")
    title = TextAttr(font_size="16pt", color="#1763cf")
    total = TextAttr(font_size="14pt")
    seller, buyer, totals = invoice_data["seller"], invoice_data["buyer"], invoice_data["totals"]
    in_tax_currency = [L.row(RowAttr(gap="xs"), [
        L.text(muted, ["VAT in"]), L.text(muted, [totals["taxCurrency"]]), L.text(muted, [totals["vatInTaxCurrency"]]),
    ])] if "vatInTaxCurrency" in totals else []
    return L.document(DocumentAttr(
        size="a4", font="body",
        assets=DocumentAssets(fonts=[FontAttr(name="body", src="../assets/fonts/SourceSans3-Regular.otf")]),
        meta=DocumentMeta(title="Invoice", author="Northwind Paper SAS", lang="en"),
    ), [
        L.section(NoAttr, [
            L.layout(LayoutAttr(margin="48pt"), [
                L.column(ColumnAttr(gap="l"), [
                    L.row(RowAttr(align="end"), [
                        L.column(ColumnAttr(width="fill", gap="xs"), [
                            L.text(TextAttr(font_size="20pt"), [seller["name"]]),
                            L.text(muted, [seller["street"]]),
                            L.row(RowAttr(gap="xs"), [L.text(muted, [seller["postcode"]]), L.text(muted, [seller["city"]])]),
                            L.row(RowAttr(gap="xs"), [L.text(muted, ["VAT"]), L.text(muted, [seller["vatId"]])]),
                        ]),
                        L.row(RowAttr(gap="xs"), [L.text(title, [invoice_data["typeCode"]]), L.text(title, [invoice_data["number"]])]),
                    ]),
                    L.divider(DividerAttr(color="#dde3ed", thickness="0.5pt")),
                    L.row(RowAttr(gap="l"), [
                        L.column(ColumnAttr(width="fill", gap="xs"), [
                            L.text(muted, ["Billed to"]),
                            L.text(NoAttr, [buyer["name"]]),
                            L.text(NoAttr, [buyer["street"]]),
                            L.row(RowAttr(gap="xs"), [L.text(NoAttr, [buyer["postcode"]]), L.text(NoAttr, [buyer["city"]])]),
                        ]),
                        L.column(ColumnAttr(width="fill", gap="xs"), [
                            L.text(muted, ["Issued · Due"]),
                            L.text(NoAttr, [invoice_data["issued"]]),
                            *[L.row(NoAttr, [L.text(NoAttr, [term["due"]])]) for term in invoice_data["paymentTerms"]],
                        ]),
                    ]),
                    L.table(TableAttr(cols="4fr 1fr 1fr 1fr 1fr 1fr"), [
                        L.thead(NoAttr, [
                            L.td(NoAttr, [L.text(muted, ["Item"])]),
                            L.td(NoAttr, [L.text(muted_right, ["Qty"])]),
                            L.td(NoAttr, [L.text(muted_right, ["Unit"])]),
                            L.td(NoAttr, [L.text(muted_right, ["Price"])]),
                            L.td(NoAttr, [L.text(muted_right, ["VAT %"])]),
                            L.td(NoAttr, [L.text(muted_right, ["Amount"])]),
                        ]),
                        *[L.tr(NoAttr, [
                            L.td(NoAttr, [L.text(NoAttr, [line["name"]])]),
                            L.td(NoAttr, [L.text(right, [line["quantity"]])]),
                            L.td(NoAttr, [L.text(right, [line["unit"]])]),
                            L.td(NoAttr, [L.text(right, [line["unitPrice"]])]),
                            L.td(NoAttr, [L.text(right, [line["vatRate"]])]),
                            L.td(NoAttr, [L.text(right, [line["net"]])]),
                        ]) for line in invoice_data["lines"]],
                    ]),
                    L.divider(DividerAttr(color="#dde3ed", thickness="0.5pt")),
                    L.table(TableAttr(cols="1fr 1fr 1fr"), [
                        L.thead(NoAttr, [
                            L.td(NoAttr, [L.text(muted, ["VAT rate (%)"])]),
                            L.td(NoAttr, [L.text(muted_right, ["Basis"])]),
                            L.td(NoAttr, [L.text(muted_right, ["VAT"])]),
                        ]),
                        *[L.tr(NoAttr, [
                            L.td(NoAttr, [L.text(NoAttr, [tax["rate"]])]),
                            L.td(NoAttr, [L.text(right, [tax["basis"]])]),
                            L.td(NoAttr, [L.text(right, [tax["amount"]])]),
                        ]) for tax in invoice_data["taxes"]],
                    ]),
                    L.column(ColumnAttr(gap="xs", align="end"), [
                        L.row(RowAttr(gap="xs"), [L.text(NoAttr, ["VAT"]), L.text(NoAttr, [totals["vat"]]), L.text(NoAttr, [totals["currency"]])]),
                        *in_tax_currency,
                        L.row(RowAttr(gap="xs"), [L.text(total, ["Total"]), L.text(total, [totals["gross"]]), L.text(total, [totals["currency"]])]),
                    ]),
                    L.text(muted, [NOTE]),
                ]),
            ]),
        ]),
    ])


@needs_fixtures
def test_fills_the_template_with_the_invoice_and_gives_the_pdf_core_gives():
    pdf = LCrossIndustryInvoice.generate_pdf(engine(), template(), invoice_xml=invoice("en16931.xml"),
                                             data={"note": NOTE}, created_on=CREATED_ON)
    compare_or_update("showcase-cross-industry-invoice", pdf)
    assert b"<pdfaid:part>3</pdfaid:part>" in pdf
    assert b"<fx:DocumentFileName>factur-x.xml</fx:DocumentFileName>" in pdf


@needs_fixtures
def test_gives_the_same_page_from_the_template_and_from_the_document_built_in_code():
    invoice_xml = invoice("en16931.xml")
    from_template = LCrossIndustryInvoice.generate_pdf(engine(), template(), invoice_xml=invoice_xml, format=FORMAT,
                                                       data={"note": NOTE}, created_on=CREATED_ON)
    invoice_data = LCrossIndustryInvoice.extract_invoice_data(invoice_xml, format=FORMAT)
    from_code = LCrossIndustryInvoice.generate_pdf(engine(), document_in_code(invoice_data), invoice_xml=invoice_xml,
                                                   created_on=CREATED_ON)
    assert from_code == from_template


@needs_fixtures
def test_extracts_the_values_core_reads_and_formats_them_by_type_and_entry_name():
    expected = json.loads((FACTURX / "case-vat-rates.json").read_text(encoding="utf-8"))
    assert LCrossIndustryInvoice.extract_invoice_data(invoice("case-vat-rates.xml")) == expected
    formatted = LCrossIndustryInvoice.extract_invoice_data(invoice("en16931.xml"), format=FORMAT)
    assert formatted["issued"] == "31 October 2026"
    assert formatted["typeCode"] == "Invoice"
    assert formatted["lines"][0]["unit"] == "pcs"
    assert formatted["totals"]["gross"] == "69.60"
    assert formatted["paymentTerms"][0]["due"] == "30 November 2026"


@needs_fixtures
def test_reads_through_a_map_given_as_text_or_bytes_under_its_own_names():
    invoice_map = ('<cross-industry-invoice-map prefix="rechnung">'
                   '<value name="nummer" path="rsm:ExchangedDocument/ram:ID"/></cross-industry-invoice-map>')
    xml = invoice("en16931.xml").decode("utf-8")
    assert LCrossIndustryInvoice.extract_invoice_data(xml, invoice_map=invoice_map) == {"nummer": "2026-0412"}
    assert LCrossIndustryInvoice.extract_invoice_data(xml, invoice_map=invoice_map.encode()) == {"nummer": "2026-0412"}


def test_gives_the_default_map_as_xml_text():
    invoice_map = LCrossIndustryInvoice.default_invoice_map()
    assert invoice_map.startswith("<?xml")
    assert '<cross-industry-invoice-map prefix="invoice">' in invoice_map


@needs_fixtures
def test_refuses_what_the_engine_refuses_with_its_error():
    with pytest.raises(EngineException, match="the invoice's profile is MINIMUM"):
        LCrossIndustryInvoice.extract_invoice_data(invoice("minimum.xml"))
    typo = template().replace("invoice:seller.name", "invoice:sellr.name")
    with pytest.raises(EngineException, match="'sellr' is not in the map"):
        LCrossIndustryInvoice.generate_pdf(engine(), typo, invoice_xml=invoice("en16931.xml"), created_on=CREATED_ON)


@needs_fixtures
def test_refuses_arguments_of_the_wrong_kind():
    with pytest.raises(TypeError):
        LCrossIndustryInvoice.extract_invoice_data(42)
    with pytest.raises(TypeError):
        LCrossIndustryInvoice.extract_invoice_data(invoice("en16931.xml"), format={"date": str})
