from __future__ import annotations

from .canvas.circle_node import CircleNode
from .canvas.ellipse_node import EllipseNode
from .canvas.image_node import ImageNode
from .canvas.layer_attr import LayerAttr
from .canvas.layer_node import LayerNode
from .canvas.line_node import LineNode
from .canvas.path_node import PathNode
from .canvas.rect_node import RectNode
from .canvas.run import Run
from .canvas.styles import EllipseStyle, LineStyle, PathStyle, RectStyle
from .canvas.text_node import CanvasTextNode
from .canvas.text_style import TextStyle
from .engine.engine_options import EngineOptions
from .kit.document import PdfDocument
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
from .layout.field_type import FieldType
from .layout.flank_attr import FlankAttr
from .layout.frame_attr import FrameAttr
from .layout.grid_attr import GridAttr
from .layout.img_attr import ImgAttr
from .layout.img_node import ImgNode
from .layout.link_attr import LinkAttr
from .layout.pin import Pin
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
from .pdf_engine import PdfEngine
from .shared.attrs_helper import options_to_attrs

NoAttr = None


class L:
    """Flat entry point for building and rendering lpdf documents."""

    # ── Engine ─────────────────────────────────────────────────────────────────

    @staticmethod
    def engine(options: EngineOptions | None = None) -> PdfEngine:
        """Create a new PdfEngine instance."""
        return PdfEngine(options)

    # ── Document / section ─────────────────────────────────────────────────────

    @staticmethod
    def document(
        attrs: DocumentAttr | None = None,
        sections: list[SectionNode] | None = None,
    ) -> PdfDocument:
        """Build the root document node."""
        a = attrs
        doc_attrs: dict = {}
        if a is not None:
            for field in ("size", "orientation", "margin", "background"):
                val = getattr(a, field, None)
                if val is not None:
                    doc_attrs[field] = val
            if getattr(a, "tokens", None) is not None:
                doc_attrs["tokens"] = a.tokens.to_dict()
            if getattr(a, "meta", None) is not None:
                doc_attrs["meta"] = a.meta.to_dict()
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
    def link(attrs: LinkAttr | None = None, nodes: list | None = None) -> ContainerNode:
        return ContainerNode("link", options_to_attrs(attrs), nodes or [])

    # ── Table ──────────────────────────────────────────────────────────────────

    @staticmethod
    def table(attrs: TableAttr | None = None, nodes: list | None = None) -> ContainerNode:
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
        flat = options_to_attrs(attrs)
        return RegionNode(flat, nodes or [])

    @staticmethod
    def field(
        field_type: str | FieldType,
        name: str,
        attrs: FieldAttr | None = None,
    ) -> FieldNode:
        fa: dict[str, str] = {"type": str(field_type), "name": name}
        fa.update(options_to_attrs(attrs))
        return FieldNode(fa)

    # ── Canvas ─────────────────────────────────────────────────────────────────

    @staticmethod
    def layer(attrs: LayerAttr | None = None, nodes: list | None = None) -> LayerNode:
        return LayerNode(nodes=nodes or [], options=attrs)

    @staticmethod
    def rect(x: float, y: float, w: float, h: float, style: RectStyle | None = None) -> RectNode:
        return RectNode(x, y, w, h, style)

    @staticmethod
    def line(x1: float, y1: float, x2: float, y2: float, style: LineStyle | None = None) -> LineNode:
        return LineNode(x1, y1, x2, y2, style)

    @staticmethod
    def ellipse(cx: float, cy: float, rx: float, ry: float, style: EllipseStyle | None = None) -> EllipseNode:
        return EllipseNode(cx, cy, rx, ry, style)

    @staticmethod
    def circle(cx: float, cy: float, r: float, style: EllipseStyle | None = None) -> CircleNode:
        return CircleNode(cx, cy, r, style)

    @staticmethod
    def path(d: str, style: PathStyle | None = None) -> PathNode:
        return PathNode(d, style)

    @staticmethod
    def text_at(
        x: float,
        y: float,
        content: str,
        style: TextStyle | None = None,
        runs: list[Run] | None = None,
    ) -> CanvasTextNode:
        return CanvasTextNode(x, y, content, style, runs)

    @staticmethod
    def img_at(x: float, y: float, w: float, h: float, name: str, anchor: str | None = None) -> ImageNode:
        return ImageNode(x, y, w, h, name, anchor)
