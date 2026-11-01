"""The ``src`` of a font, an image, a file and a file of Markdown rules is found in an XML document as the engine
reads the document: entities decoded, a ``>`` in a quoted value, either quote, and what is in a comment or a CDATA
section is text. Each render goes to a stand-in for the engine, which keeps the request it is sent."""

import base64
from pathlib import Path
from unittest.mock import patch

import pytest

from lpdf import PdfEngine

RED_TITLES = '<markdown-styles><h1 color="#ff0000"/></markdown-styles>'


def _xml(assets: str = "", attachments: str = "", section: str = "<layout><text>x</text></layout>") -> str:
    return (f'<lpdf version="1"><assets>{assets}</assets><document><attachments>{attachments}</attachments>'
            f"<section>{section}</section></document></lpdf>")


def _request(xml: str) -> dict:
    """The request a render of ``xml`` sends the engine."""
    with patch("lpdf.engine.wasm_runner.WasmRunner.invoke", return_value={"pdf": "JVBERi0="}) as invoke:
        PdfEngine().set_license_key("test-key").render(xml)
    return invoke.call_args.args[0]


@pytest.mark.parametrize(("kind", "declaration", "file", "key"), [
    pytest.param("fonts", '<font name="brand" ref="R&amp;D Sans" src="{dir}/R&amp;D Sans.ttf"/>', "R&D Sans.ttf", "R&D Sans", id="a font with an entity"),
    pytest.param("fonts", '<font name="brand" ref="rows > 1000" src="{dir}/brand.ttf"/>', "brand.ttf", "rows > 1000", id="a font after a >"),
    pytest.param("fonts", "<font name='brand' src='{dir}/brand.ttf'/>", "brand.ttf", "brand", id="a font in single quotes"),
    pytest.param("images", '<image name="logo" ref="R&amp;D logo" src="{dir}/R&amp;D logo.png"/>', "R&D logo.png", "R&D logo", id="an image with an entity"),
    pytest.param("images", '<image name="logo" ref="rows > 1000" src="{dir}/logo.png"/>', "logo.png", "rows > 1000", id="an image after a >"),
    pytest.param("images", "<image name='logo' src='{dir}/logo.png'/>", "logo.png", "logo", id="an image in single quotes"),
    pytest.param("files", '<file name="R&amp;D.csv" src="{dir}/R&amp;D.csv"/>', "R&D.csv", "R&D.csv", id="a file with an entity"),
    pytest.param("files", '<file name="rows.csv" description="rows > 1000" src="{dir}/rows.csv"/>', "rows.csv", "rows.csv", id="a file after a >"),
    pytest.param("files", "<file name='rows.csv' src='{dir}/rows.csv'/>", "rows.csv", "rows.csv", id="a file in single quotes"),
])
def test_a_src_is_read_and_loaded_under_its_ref_or_name(tmp_path: Path, kind: str, declaration: str, file: str, key: str) -> None:
    (tmp_path / file).write_bytes(f"the bytes of {file}".encode())
    declaration = declaration.replace("{dir}", str(tmp_path))

    request = _request(_xml(attachments=declaration) if kind == "files" else _xml(assets=declaration))

    assert request.get(kind) == {key: base64.b64encode(f"the bytes of {file}".encode()).decode()}


@pytest.mark.parametrize(("styles", "file"), [
    pytest.param('<markdown-styles src="{dir}/R&amp;D styles.xml"/>', "R&D styles.xml", id="with an entity"),
    pytest.param('<markdown-styles xmlns:rows="urn:rows>1000" src="{dir}/styles.xml"/>', "styles.xml", id="after a >"),
    pytest.param("<markdown-styles src='{dir}/styles.xml'/>", "styles.xml", id="in single quotes"),
])
def test_a_file_of_rules_is_read_from_the_src_of_its_styles(tmp_path: Path, styles: str, file: str) -> None:
    (tmp_path / file).write_text(RED_TITLES, encoding="utf-8")
    styles = styles.replace("{dir}", str(tmp_path))

    request = _request(_xml(section=f"<markdown>{styles}<markdown-content># Title</markdown-content></markdown>"))

    assert request.get("markdown_styles") == {f"{tmp_path}/{file}": RED_TITLES}


@pytest.mark.parametrize("declaration", [
    pytest.param('<assets><font name="brand" src="{dir}/hidden"/></assets>', id="a font"),
    pytest.param('<assets><image name="logo" src="{dir}/hidden"/></assets>', id="an image"),
    pytest.param('<attachments><file name="rows.csv" src="{dir}/hidden"/></attachments>', id="a file"),
    pytest.param('<markdown><markdown-styles src="{dir}/hidden"/></markdown>', id="a file of rules"),
])
def test_a_src_in_a_comment_or_a_cdata_section_is_text_and_is_not_read(tmp_path: Path, declaration: str) -> None:
    (tmp_path / "hidden").write_text("hidden", encoding="utf-8")
    declaration = declaration.replace("{dir}", str(tmp_path))

    request = _request(_xml(section=f"<layout><!-- {declaration} --><code><![CDATA[{declaration}]]></code></layout>"))

    assert not {"fonts", "images", "files", "markdown_styles"} & request.keys()
