"""
example.py — render every example in lpdf's examples/ folder.

An example is a folder examples/<n>-<id>/ with its document.xml, its document.json if it has data, and the
fonts and images its <assets> name, by paths relative to the folder. Each is rendered the way the docs on
lpdf.io render it: a fresh engine, those fonts and images loaded, and the data passed to render.

Run from lpdf's root (after 'make build-sdk-python'):
  make example-python

Output: tmp/sdk-examples/<n>-<id>-python.pdf in lpdf's root.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lpdf import L, RenderOptions

# lpdf's root: /app in make's container, which mounts examples/ and tmp/sdk-examples/ there;
# three folders up when run from repos/lpdf-python/example
lpdf = Path("/app") if Path("/.dockerenv").exists() else Path(__file__).resolve().parents[3]
output = lpdf / "tmp/sdk-examples"
output.mkdir(parents=True, exist_ok=True)

folders = sorted(
    (folder for folder in (lpdf / "examples").iterdir() if folder.is_dir() and re.match(r"\d+-", folder.name)),
    key=lambda folder: int(folder.name.split("-")[0]),
)

for folder in folders:
    xml = (folder / "document.xml").read_text(encoding="utf-8")
    data_file = folder / "document.json"
    data = json.loads(data_file.read_bytes()) if data_file.exists() else None

    # init engine: a fresh one for each example, so a font one of them names does not reach the next
    engine = L.engine()  # no key → renders with the attribution line

    # load the fonts and images the document names; its comments may name others, to show the format
    body = re.sub(r"<!--.*?-->", "", xml, flags=re.DOTALL)
    for font, src in re.findall(r'<font\s+name="([^"]+)"\s+src="([^"]+)"', body):
        engine.load_font(font, (folder / src).read_bytes())
    for image, src in re.findall(r'<image\s+name="([^"]+)"\s+src="([^"]+)"', body):
        engine.load_image(image, (folder / src).read_bytes())

    # render pdf from xml, with the example's data if it has any
    pdf = engine.render(xml) if data is None else engine.render(xml, options=RenderOptions(data=data))

    # write pdf to file
    output_file = f"{folder.name}-python.pdf"
    (output / output_file).write_bytes(pdf)

    print(f"output: {output_file} ({len(pdf):,} bytes)")
