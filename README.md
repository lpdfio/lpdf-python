<img src="https://raw.githubusercontent.com/lpdfio/lpdf-python/main/lpdf-mark.svg" height="48" alt="Lpdf - PDF as Code" />

# lpdfio-lpdf

**Python SDK for [Lpdf](https://lpdf.io?utm_campaign=sdk-python&utm_medium=referral&utm_source=readme) — PDF as Code on every platform**

You describe a document as code or XML. Lpdf renders a compact, pixel-perfect PDF — identical across platforms.

## Installation

```bash
pip install lpdfio-lpdf
```

`pip install` is the whole setup. The engine runs inside Python on the [`wasmtime`](https://pypi.org/project/wasmtime/) package, which pip installs with the SDK: there is no program to install or put on `PATH`.

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

A render releases the GIL, so renders on threads run in parallel: use a thread pool, or `asyncio.to_thread` in async code. A render stops with an `EngineException` after 30 seconds; `L.engine(EngineOptions(timeout=60))` sets another limit in seconds, and `timeout=0` sets none.

## Requirements

- Python 3.11+
- A platform the `wasmtime` package has wheels for: Linux (x86_64, aarch64; glibc and musl), macOS (x86_64, arm64) or Windows (x64, arm64)

## Docs

[lpdf.io/docs](https://lpdf.io/docs/install/?sdk=python&utm_campaign=sdk-python&utm_medium=referral&utm_source=readme)

## Issues

Report bugs and request features at [github.com/lpdfio/lpdf/issues](https://github.com/lpdfio/lpdf/issues), the one tracker for the engine, the SDKs and the VS Code extension. Pull requests are not accepted.

--

Dual-licensed: Community License (free) and Commercial License (paid). See [LICENSE](LICENSE) for full terms.
