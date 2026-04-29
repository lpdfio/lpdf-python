import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lpdf import Pdf

_docker_root = Path("/app/example-data")
root = _docker_root if _docker_root.exists() else Path(__file__).resolve().parents[4] / "example"

examples = [
    "example1",
    "example2",
    "example-contract",
]

# init engine
engine = Pdf.engine()  # no key → free tier (watermark)

# load assets (only used if referenced in xml/layout)
engine.load_font("montserrat", (root / "assets/fonts/Montserrat-Regular.ttf").read_bytes())
engine.load_image("logo", (Path(__file__).resolve().parent.parent / "lpdf-light.png").read_bytes())

for example in examples:
    # load xml from file
    xml = (root / "xml" / f"{example}.xml").read_text(encoding="utf-8")

    # render pdf from xml
    pdf = engine.render(xml)

    # define output file name
    output_file = f"{example}-python.pdf"

    # write pdf to file
    (root / "result" / output_file).write_bytes(pdf)

    print(f"output: {output_file} ({len(pdf):,} bytes)")
