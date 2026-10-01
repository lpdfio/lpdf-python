from __future__ import annotations

import json

from .canvas.canvas_img_attr import CanvasImgAttr
from .canvas.canvas_text_attr import CanvasTextAttr
from .canvas.circle_attr import CircleAttr
from .canvas.circle_node import CircleNode
from .canvas.ellipse_attr import EllipseAttr
from .canvas.ellipse_node import EllipseNode
from .canvas.image_node import ImageNode
from .canvas.layer_attr import LayerAttr
from .canvas.layer_node import LayerNode
from .canvas.line_attr import LineAttr
from .canvas.line_node import LineNode
from .canvas.path_attr import PathAttr
from .canvas.path_node import PathNode
from .canvas.rect_attr import RectAttr
from .canvas.rect_node import RectNode
from .canvas.text_node import CanvasTextNode
from .engine.engine_exception import EngineException
from .engine.engine_options import EngineOptions
from .engine.wasm_runner import WasmRunner
from .kit.document import PdfDocument
from .kit.document_assets import DocumentAssets
from .kit.document_attr import DocumentAttr
from .kit.document_tokens import DocumentTokens
from .kit.section_attr import SectionAttr
from .kit.section_canvas import SectionCanvas
from .kit.section_layout import SectionLayout
from .kit.section_node import SectionNode
from .layout.barcode_attr import BarcodeAttr
from .layout.barcode_node import BarcodeNode
from .layout.cluster_attr import ClusterAttr
from .layout.container_node import ContainerNode
from .layout.divider_attr import DividerAttr
from .layout.divider_node import DividerNode
from .layout.field_attr import FieldAttr
from .layout.field_node import FieldNode
from .layout.flank_attr import FlankAttr
from .layout.frame_attr import FrameAttr
from .layout.grid_attr import GridAttr
from .layout.img_attr import ImgAttr
from .layout.img_node import ImgNode
from .layout.link_attr import LinkAttr
from .layout.region_attr import RegionAttr
from .layout.region_node import RegionNode
from .layout.span_attr import SpanAttr
from .layout.span_node import SpanNode
from .layout.split_attr import SplitAttr
from .layout.stack_attr import StackAttr
from .layout.table_attr import TableAttr
from .layout.td_attr import TdAttr
from .layout.text_attr import TextAttr
from .layout.text_node import TextNode
from .layout.thead_attr import TheadAttr
from .layout.tr_attr import TrAttr
from .pdf_engine import PdfEngine, default_wasm_binary
from .shared.attrs_helper import options_to_attrs

NoAttr = None


class L:
    """Flat entry point for building and rendering lpdf documents."""

    # ── Engine ─────────────────────────────────────────────────────────────────

    @staticmethod
    def engine(options: EngineOptions | None = None) -> PdfEngine:
        """Create a new PdfEngine instance."""
        return PdfEngine(options)

    # ── XML conversion ─────────────────────────────────────────────────────────

    @staticmethod
    def to_xml(document: PdfDocument) -> str:
        """Convert a document tree to an lpdf XML string without rendering it."""
        runner = WasmRunner(wasm_binary=default_wasm_binary())
        response = runner.invoke({
            "method": "kit_to_xml",
            "key": "",
            "input": json.dumps(document.to_dict(), ensure_ascii=False),
        })
        if "xml" not in response:
            raise EngineException("Unexpected response from WASI kit_to_xml call.")
        return response["xml"]

    # ── Document / section ─────────────────────────────────────────────────────

    @staticmethod
    def document(
        attrs: DocumentAttr | None = None,
        sections: list[SectionNode] | None = None,
    ) -> PdfDocument:
        """Build the root document node."""
        doc_attrs: dict = options_to_attrs(attrs)
        if attrs is not None and attrs.assets is not None:
            doc_attrs["assets"] = attrs.assets.to_dict()
        if attrs is not None and attrs.tokens is not None:
            doc_attrs["tokens"] = attrs.tokens.to_dict()
        if attrs is not None and attrs.meta is not None:
            doc_attrs["meta"] = attrs.meta.to_dict()
        return PdfDocument(doc_attrs, sections or [])

    @staticmethod
    def section(
        attrs: SectionAttr | None = None,
        nodes: list | None = None,
    ) -> SectionNode:
        """Build a section (page) node."""
        return SectionNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def layout(_attrs: object, nodes: list | None = None) -> SectionLayout:
        """Wrap layout nodes into a layout block."""
        return SectionLayout(nodes or [])

    @staticmethod
    def canvas(_attrs: object, layers: list | None = None) -> SectionCanvas:
        """Wrap canvas layer nodes into a canvas block."""
        return SectionCanvas(layers or [])

    @staticmethod
    def assets(attrs: DocumentAssets) -> DocumentAssets:
        """Create a DocumentAssets instance (convenience factory)."""
        return attrs

    @staticmethod
    def tokens(attrs: DocumentTokens) -> DocumentTokens:
        """Create a DocumentTokens instance (convenience factory)."""
        return attrs

    # ── Layout containers ──────────────────────────────────────────────────────

    @staticmethod
    def stack(attrs: StackAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("stack", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def flank(attrs: FlankAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("flank", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def split(attrs: SplitAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("split", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def cluster(attrs: ClusterAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("cluster", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def grid(attrs: GridAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("grid", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def frame(attrs: FrameAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("frame", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def link(attrs: LinkAttr, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("link", options_to_attrs(attrs), nodes or [])

    # ── Table ──────────────────────────────────────────────────────────────────

    @staticmethod
    def table(attrs: TableAttr, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("table", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def thead(attrs: TheadAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("thead", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def tr(attrs: TrAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("tr", options_to_attrs(attrs), nodes or [])

    @staticmethod
    def td(attrs: TdAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("td", options_to_attrs(attrs), nodes or [])

    # ── Layout leaves ──────────────────────────────────────────────────────────

    @staticmethod
    def text(attrs: TextAttr | None = None, nodes: list | None = None) -> TextNode:
        """Build a text paragraph node. Children must be strings or SpanNode instances."""
        return TextNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def span(attrs: SpanAttr | None = None, nodes: list[str] | None = None) -> SpanNode:
        """Build a span inline node. Children must be plain strings."""
        return SpanNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def divider(attrs: DividerAttr | None = None) -> DividerNode:
        return DividerNode(options_to_attrs(attrs))

    @staticmethod
    def img(attrs: ImgAttr) -> ImgNode:
        return ImgNode(options_to_attrs(attrs))

    @staticmethod
    def barcode(attrs: BarcodeAttr) -> BarcodeNode:
        return BarcodeNode(options_to_attrs(attrs))

    @staticmethod
    def region(attrs: RegionAttr, nodes: list | None = None) -> RegionNode:
        """Build a pinned region node. attrs.pin is required."""
        return RegionNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def field(attrs: FieldAttr) -> FieldNode:
        """Build a form field node. attrs.type and attrs.name are required."""
        return FieldNode(options_to_attrs(attrs))

    # ── Canvas ─────────────────────────────────────────────────────────────────

    @staticmethod
    def layer(attrs: LayerAttr | None = None, nodes: list | None = None) -> LayerNode:
        return LayerNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def rect(attrs: RectAttr) -> RectNode:
        return RectNode(options_to_attrs(attrs))

    @staticmethod
    def line(attrs: LineAttr) -> LineNode:
        return LineNode(options_to_attrs(attrs))

    @staticmethod
    def ellipse(attrs: EllipseAttr) -> EllipseNode:
        return EllipseNode(options_to_attrs(attrs))

    @staticmethod
    def circle(attrs: CircleAttr) -> CircleNode:
        return CircleNode(options_to_attrs(attrs))

    @staticmethod
    def path(attrs: PathAttr) -> PathNode:
        return PathNode(options_to_attrs(attrs))

    @staticmethod
    def text_at(attrs: CanvasTextAttr, nodes: list | None = None) -> CanvasTextNode:
        """Build text on the canvas. Children must be strings or SpanNode instances."""
        return CanvasTextNode(options_to_attrs(attrs), nodes or [])

    @staticmethod
    def img_at(attrs: CanvasImgAttr) -> ImageNode:
        return ImageNode(options_to_attrs(attrs))
