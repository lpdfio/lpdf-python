"""
encrypt-open-password.py — render showcase-encryption.xml with RC4-128 encryption,
open password required, copy disabled.

Run from lpdf's root (after 'make build-sdk-python'):
  make example-python

Output: tmp/sdk-examples/encrypt-open-password-python.pdf in lpdf's root.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lpdf import L

# lpdf's root: /app in make's container, which mounts test/fixtures/ and tmp/sdk-examples/ there;
# three folders up when run from repos/lpdf-python/example
lpdf = Path("/app") if Path("/.dockerenv").exists() else Path(__file__).resolve().parents[3]
xml_file = lpdf / "test/fixtures/showcase-encryption.xml"
output = lpdf / "tmp/sdk-examples"

output_file = "encrypt-open-password-python.pdf"

xml = xml_file.read_text(encoding="utf-8")

engine = L.engine()  # no key → renders with the attribution line

# With open password — viewers prompt for "password" before displaying content.
engine.set_encryption("password", "owner", {"copy": False})

pdf = engine.render(xml)

output.mkdir(parents=True, exist_ok=True)
(output / output_file).write_bytes(pdf)
print(f"output: {output_file} ({len(pdf):,} bytes)")
