<p align="center"><img src="lpdf-light.png" height="48" alt="Lpdf"></p>

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

## Docs

[lpdf.io/docs/python](https://lpdf.io/docs/python)

--

Dual-licensed: Community License (free) and Commercial License (paid). See [LICENSE](LICENSE) for full terms.
