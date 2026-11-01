FROM python:3.11-slim

# The engine runs inside Python on the wasmtime package, which pip installs with the SDK: no wasmtime program.
RUN pip install --no-cache-dir pytest "wasmtime>=50"

WORKDIR /app

COPY src/lpdf/ ./lpdf/
COPY tests/ ./tests/
COPY resources/ ./resources/
