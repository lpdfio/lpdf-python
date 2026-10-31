from __future__ import annotations

import base64
import contextlib
import json
import re
import secrets
import time
from pathlib import Path

from .engine.engine_exception import EngineException
from .engine.engine_options import EngineOptions
from .engine.render_options import RenderOptions
from .engine.wasm_runner import WasmRunner
from .kit.document import PdfDocument


def _tree_asset_srcs(attrs: dict, kind: str) -> dict[str, str]:
    """The ``ref or name -> src`` pairs of the fonts or images a document tree declares in ``assets``."""
    declared = (attrs.get("assets") or {}).get(kind) or []
    return {item.get("ref") or item["name"]: item["src"] for item in declared if item.get("src")}


_ENTROPY_BYTES = 32


def _encryption_payload(options: RenderOptions | None) -> dict:
    """The passwords and ``skip_encryption`` of a render request, as given. With a password, AES-256 needs random
    bytes, which the engine does not make: they come from the operating system's secure generator, fresh for each
    render."""
    if options is None:
        return {}
    payload: dict = {}
    if options.user_password is not None:
        payload["user_password"] = options.user_password
    if options.owner_password is not None:
        payload["owner_password"] = options.owner_password
    if payload:
        payload["entropy"] = base64.b64encode(secrets.token_bytes(_ENTROPY_BYTES)).decode()
    if options.skip_encryption:
        payload["skip_encryption"] = True
    return payload


def _load_declared(srcs: dict[str, str], loaded: dict[str, bytes]) -> None:
    """Read each declared file that is not already loaded on the engine; one that cannot be read is skipped."""
    for key, src in srcs.items():
        if key not in loaded:
            with contextlib.suppress(OSError):
                loaded[key] = Path(src).read_bytes()


def _extract_xml_font_srcs(xml: str) -> dict[str, str]:
    srcs = {}
    for tag in re.findall(r'<font\s[^>]*>', xml):
        name = re.search(r'\bname="([^"]*)"', tag)
        ref  = re.search(r'\bref="([^"]*)"',  tag)
        src  = re.search(r'\bsrc="([^"]*)"',  tag)
        if name and src:
            key = ref.group(1) if ref else name.group(1)
            srcs[key] = src.group(1)
    return srcs


def _extract_xml_image_srcs(xml: str) -> dict[str, str]:
    srcs = {}
    for tag in re.findall(r'<image\s[^>]*>', xml):
        name = re.search(r'\bname="([^"]*)"', tag)
        ref  = re.search(r'\bref="([^"]*)"',  tag)
        src  = re.search(r'\bsrc="([^"]*)"',  tag)
        if name and src:
            key = ref.group(1) if ref else name.group(1)
            srcs[key] = src.group(1)
    return srcs


def _extract_xml_markdown_styles_srcs(xml: str) -> list[str]:
    """The ``src`` of each ``<markdown-styles>`` in XML."""
    srcs = []
    for tag in re.findall(r'<markdown-styles\s[^>]*>', xml):
        src = re.search(r'\bsrc="([^"]*)"', tag)
        if src and src.group(1):
            srcs.append(src.group(1))
    return srcs


def _tree_markdown_styles_srcs(document: dict) -> list[str]:
    """The ``src`` of each ``markdown-styles`` in the markdown of any section of a document tree."""
    srcs = []
    for section in document.get("nodes") or []:
        for child in section.get("nodes") or []:
            if child.get("type") != "markdown":
                continue
            for part in child.get("nodes") or []:
                src = (part.get("attrs") or {}).get("src")
                if part.get("type") == "markdown-styles" and src:
                    srcs.append(src)
    return srcs


def default_wasm_binary() -> str:
    """The path of the WASI binary the SDK ships."""
    return str(Path(__file__).resolve().parent.parent / "resources" / "lpdf-wasi.wasm")


class PdfEngine:
    def __init__(self, options: EngineOptions | None = None):
        self._license_key: str = ""
        self._options = options or EngineOptions()
        self._fonts: dict[str, bytes] = {}
        self._images: dict[str, bytes] = {}
        self._markdown_styles: dict[str, str] = {}

    def set_license_key(self, key: str) -> PdfEngine:
        self._license_key = key
        return self

    def check_license_key(self, key: str | None = None) -> dict:
        """Ask the engine what a license key is.

        Returns the engine's report: ``status`` always — one of ``licensed``, ``no_key``,
        ``expired``, ``version_mismatch``, ``wrong_product``, ``unknown_key``,
        ``bad_signature`` or ``malformed`` — plus ``product``, ``tier``, ``expires``,
        ``license`` and ``key`` once the signature verified.

        This is the engine's own verdict, from the same code a render runs, so ``licensed``
        means PDFs come out without the attribution line here. A key the portal considers
        perfectly good still reads ``unknown_key`` in a build that does not trust the key it
        was signed with, which is the answer worth having.

        :param key: The key to check. Defaults to the one set on this engine.
        """
        runner = WasmRunner(
            wasm_binary=self._options.wasm_binary or self._default_binary(),
            wasm_runner=self._options.wasm_runner or "wasmtime",
            timeout=self._options.timeout or 30,
        )
        return runner.invoke({
            "method": "check_license",
            "key": key if key is not None else self._license_key,
            "now": int(time.time()),
        })

    def load_font(self, name: str, data: bytes) -> PdfEngine:
        self._fonts[name] = data
        return self

    def load_image(self, name: str, data: bytes) -> PdfEngine:
        self._images[name] = data
        return self

    def load_markdown_styles(self, src: str, text: str) -> PdfEngine:
        """Register the text of a file of Markdown rules, the root of which is a ``<markdown-styles>``, for the
        ``src`` that names it in ``<markdown-styles src="…">``."""
        self._markdown_styles[src] = text
        return self

    def render(
        self,
        input: str | PdfDocument,
        options: RenderOptions | None = None,
    ) -> bytes:
        if isinstance(input, PdfDocument):
            method = "render_tree_pdf"
            input_dict = input.to_dict()
            input_str = json.dumps(input_dict, ensure_ascii=False)
        else:
            method = "render_pdf"
            input_str = input
            input_dict = None

        runner = WasmRunner(
            wasm_binary=self._options.wasm_binary or self._default_binary(),
            wasm_runner=self._options.wasm_runner or "wasmtime",
            timeout=self._options.timeout or 30,
        )

        # Use load_font() fonts as base; auto-load from src= paths if not already provided.
        merged_fonts: dict[str, bytes] = dict(self._fonts)

        if input_dict is not None:
            font_srcs = _tree_asset_srcs(input_dict.get("attrs") or {}, "fonts")
        else:
            font_srcs = _extract_xml_font_srcs(input_str)
        _load_declared(font_srcs, merged_fonts)

        payload: dict = {
            "method": method,
            "key": self._license_key,
            "input": input_str,
            # The engine is WebAssembly and has no clock of its own: without this it cannot check
            # the key's expiry, and an expired key renders as though it were current.
            "now": int(time.time()),
        }

        if merged_fonts:
            payload["fonts"] = {
                name: base64.b64encode(data).decode() for name, data in merged_fonts.items()
            }

        # Images: load_image() + auto-load from src=
        merged_images: dict[str, bytes] = dict(self._images)

        if input_dict is not None:
            image_srcs = _tree_asset_srcs(input_dict.get("attrs") or {}, "images")
        else:
            image_srcs = _extract_xml_image_srcs(input_str)
        _load_declared(image_srcs, merged_images)

        if merged_images:
            payload["images"] = {
                name: base64.b64encode(data).decode() for name, data in merged_images.items()
            }

        # The files of Markdown rules a document names with a src: the ones loaded here, and the ones read from
        # the path. A file that cannot be read is left for the engine to report, naming the src.
        merged_styles: dict[str, str] = dict(self._markdown_styles)
        style_srcs = (
            _tree_markdown_styles_srcs(input_dict) if input_dict is not None else _extract_xml_markdown_styles_srcs(input_str)
        )
        for src in style_srcs:
            if src not in merged_styles:
                with contextlib.suppress(OSError):
                    merged_styles[src] = Path(src).read_text(encoding="utf-8")
        if merged_styles:
            payload["markdown_styles"] = merged_styles

        if options is not None and options.created_on is not None:
            payload["created_on"] = options.created_on

        payload.update(_encryption_payload(options))

        if options is not None and options.data is not None and method == "render_pdf":
            payload["data"] = options.data

        response = runner.invoke(payload)

        if "pdf" not in response:
            raise EngineException("Unexpected response from WASI process.")

        return base64.b64decode(response["pdf"])

    @staticmethod
    def _default_binary() -> str:
        return default_wasm_binary()
