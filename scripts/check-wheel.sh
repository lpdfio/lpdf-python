#!/bin/sh
# Installs the wheel in dist/ into a clean virtualenv and renders a document with it, so a wheel
# without the engine binary, or one that can't find it, fails here and not on a user's machine.
# The render runs with only the virtualenv on PATH: pip install is the whole setup, with no wasmtime
# program. Run from the repo root after `python -m build`.
set -eu

wheel=$(ls dist/*.whl)

if ! python -m zipfile -l "$wheel" | grep -q '^resources/lpdf-wasi.wasm'; then
  echo "::error::$wheel has no resources/lpdf-wasi.wasm. The build must find the engine in src/resources/."
  exit 1
fi

venv=$(mktemp -d)
trap 'rm -rf "$venv"' EXIT

python -m venv "$venv"
"$venv/bin/pip" install --quiet "$wheel"

# From another folder, so that lpdf comes from the wheel and not from src/.
cd "$venv"
PATH="$venv/bin" "$venv/bin/python" - <<'PY'
from lpdf import PdfEngine

pdf = PdfEngine().render('<lpdf version="1"><document><section><layout><text>wheel check</text></layout></section></document></lpdf>')
assert pdf.startswith(b"%PDF"), "the engine returned no PDF"
print(f"Rendered {len(pdf)} bytes with the installed wheel")
PY
