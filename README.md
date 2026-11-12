<img src="https://raw.githubusercontent.com/lpdfio/lpdf-python/main/lpdf-mark.svg" height="48" alt="Lpdf - PDF as Code" />

# lpdfio-lpdf

`lpdfio-lpdf` is the Python SDK for [Lpdf](https://lpdf.io?utm_campaign=sdk-python&utm_medium=referral&utm_source=readme), the PDF engine that renders a document written in XML or built in code to the same PDF in every language.

## Installation

```bash
pip install lpdfio-lpdf
```

## Usage

```python
from lpdf import L, NoAttr, DocumentAttr, LayoutAttr, ColumnAttr, RowAttr, TextAttr, DividerAttr

engine = L.engine()

doc = L.document(DocumentAttr(size='letter'), [
    L.section(NoAttr, [
        L.layout(LayoutAttr(margin='48pt'), [
            L.column(ColumnAttr(gap='24pt'), [
                L.row(RowAttr(justify='between'), [
                    L.text(TextAttr(font_size='8pt', color='#888888'), ['ACME CORP']),
                    L.text(TextAttr(font_size='22pt', bold=True), ['Project Proposal']),
                ]),
                L.divider(DividerAttr(thickness='xs')),
                L.text(TextAttr(font_size='13pt', bold=True), ['Scope of Work']),
                L.row(RowAttr(gap='12pt', align='start'), [
                    L.text(TextAttr(color='#888888', width='24pt'), ['01']),
                    L.text(TextAttr(width='fill'), ['Discovery & Research']),
                ]),
            ]),
        ]),
    ]),
])

pdf = engine.render(doc)
```

## Requirements

- Python 3.11 or later, on Linux (x86_64 or aarch64, glibc or musl), macOS (x86_64 or arm64) or Windows (x64 or arm64)
- Nothing else: the engine runs inside Python on the [`wasmtime`](https://pypi.org/project/wasmtime/) package, which pip installs with the SDK

## Docs

[lpdf.io/docs](https://lpdf.io/docs/install/?sdk=python&utm_campaign=sdk-python&utm_medium=referral&utm_source=readme)

## Issues

Report bugs and request features at [github.com/lpdfio/lpdf/issues](https://github.com/lpdfio/lpdf/issues), the one tracker for the engine, the SDKs and the VS Code extension. Pull requests are not accepted.

---

Licensed under the Lpdf License. See [LICENSE](https://github.com/lpdfio/lpdf-python/blob/main/LICENSE) for full terms.
