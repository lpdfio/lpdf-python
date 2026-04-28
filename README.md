# lpdfio-lpdf

Python adapter for [Lpdf](https://lpdf.io) — an accurate, efficient, and cross-platform PDF engine.

## Installation

```bash
pip install lpdfio-lpdf
```

## Usage

```python
from lpdf import LpdfEngine

engine = LpdfEngine("")

engine.load_font("montserrat", open("fonts/Montserrat-Regular.ttf", "rb").read())
engine.load_image("logo", open("images/logo.png", "rb").read())

xml = open("document.xml", "r", encoding="utf-8").read()
pdf = engine.render_pdf(xml)

open("output.pdf", "wb").write(pdf)
```

## XML format

Documents are defined in a layout XML format. See the [Lpdf documentation](https://lpdf.io/docs) and [examples](https://github.com/lpdfio/lpdf/tree/main/docs/examples) for the full schema.

```xml
<stack spacing="m" padding="l">
  <text font-size="xl" font="Montserrat-Bold">Invoice #1001</text>
  <grid columns="2">
    <text>Date</text>      <text>2026-04-25</text>
    <text>Due</text>       <text>2026-05-25</text>
  </grid>
</stack>
```

## Requirements

- Python 3.8+

## License

Dual-licensed: Community License (free) and Commercial License (paid). See [LICENSE](LICENSE) for full terms.
