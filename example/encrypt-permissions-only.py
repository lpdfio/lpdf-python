"""
encrypt-permissions-only.py — render showcase-encryption.xml, whose <output> asks for AES-256
and allows neither copying nor modifying, with no open password.

Run from lpdf's root (after 'make build-sdk-python'):
  make example-python

Output: tmp/sdk-examples/encrypt-permissions-only-python.pdf in lpdf's root.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lpdf import L, RenderOptions

# lpdf's root: /app in make's container, which mounts test/fixtures/ and tmp/sdk-examples/ there;
# three folders up when run from repos/lpdf-python/example
lpdf = Path("/app") if Path("/.dockerenv").exists() else Path(__file__).resolve().parents[3]
xml_file = lpdf / "test/fixtures/showcase-encryption.xml"
output = lpdf / "tmp/sdk-examples"

output_file = "encrypt-permissions-only-python.pdf"

xml = xml_file.read_text(encoding="utf-8")

engine = L.engine()  # no key → renders with the attribution line

# Permissions only — no open password.
# File opens freely; cooperative viewers enforce the allow of the document's <output>.
pdf = engine.render(xml, RenderOptions(owner_password="s3cr3t"))

output.mkdir(parents=True, exist_ok=True)
(output / output_file).write_bytes(pdf)
print(f"output: {output_file} ({len(pdf):,} bytes)")
