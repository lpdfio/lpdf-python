"""
example-data.py — render the invoice in lpdf's examples/ with its data from document.json.

Run from lpdf's root (after 'make build-sdk-python'):
  make example-python

Output: tmp/sdk-examples/example-data-python.pdf in lpdf's root.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lpdf import L, RenderOptions

# lpdf's root: /app in make's container, which mounts examples/ and tmp/sdk-examples/ there;
# three folders up when run from repos/lpdf-python/example
lpdf = Path("/app") if Path("/.dockerenv").exists() else Path(__file__).resolve().parents[3]

xml_file  = lpdf / "examples/2-invoice/document.xml"
json_file = lpdf / "examples/2-invoice/document.json"
output = lpdf / "tmp/sdk-examples"
output_file = "example-data-python.pdf"

xml  = xml_file.read_text(encoding="utf-8")
data = json.loads(json_file.read_bytes())

engine = L.engine()  # no key → renders with the attribution line

pdf = engine.render(xml, options=RenderOptions(data=data))

output.mkdir(parents=True, exist_ok=True)
(output / output_file).write_bytes(pdf)
print(f"output: {output_file} ({len(pdf):,} bytes)")
