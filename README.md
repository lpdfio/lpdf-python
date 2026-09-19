<img src="https://raw.githubusercontent.com/lpdfio/lpdf-python/main/lpdf-mark.svg" height="48" alt="Lpdf - PDF as Code" />

# lpdfio-lpdf

**Python SDK for [Lpdf](https://lpdf.io) — PDF as Code on every platform**

You describe a document as code or XML. Lpdf renders a compact, pixel-perfect PDF — identical across platforms.

## Installation

```bash
pip install lpdfio-lpdf
```

## Usage

```python
from lpdf import L, NoAttr

engine = L.engine()

doc = L.document(DocumentAttr(size='letter', margin='48pt'), [
    L.section(NoAttr, [
        L.layout(NoAttr, [
            L.stack(StackAttr(gap='24pt'), [
                L.split(NoAttr, [
                    L.text(TextAttr(font_size='8pt', color='#888888'), ['ACME CORP']),
                    L.text(TextAttr(font_size='22pt', bold='true'), ['Project Proposal']),
                ]),
                L.divider(DividerAttr(thickness='xs')),
                L.text(TextAttr(font_size='13pt', bold='true'), ['Scope of Work']),
                L.flank(FlankAttr(gap='12pt', align='start'), [
                    L.text(TextAttr(color='#888888', width='24pt'), ['01']),
                    L.text(NoAttr, ['Discovery & Research']),
                ]),
            ]),
        ]),
    ]),
])

pdf = engine.render(doc)
```

## Requirements

- Python 3.8+
- [`wasmtime`](https://wasmtime.dev) CLI must be available in `PATH` (used to run the bundled WASI binary).

## Versioning

The first two numbers are the Lpdf engine, and the last number counts changes to this package only. `0.22.3` runs engine `0.22`, with three Python-only changes since that engine shipped. Every engine release publishes all SDKs at `X.Y.0`, so the same `X.Y` means the same engine in every language.

To stay on one engine and still get this package's fixes: `pip install "lpdfio-lpdf~=0.22.0"`.

## Docs

[lpdf.io/docs/python](https://lpdf.io/docs/python)

## Issues

Report bugs and request features at [github.com/lpdfio/lpdf/issues](https://github.com/lpdfio/lpdf/issues), the one tracker for the engine, the SDKs and the VS Code extension. Pull requests are not accepted.

--

Dual-licensed: Community License (free) and Commercial License (paid). See [LICENSE](LICENSE) for full terms.
