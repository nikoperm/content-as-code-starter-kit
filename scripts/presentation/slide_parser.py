"""Slide Parser — converts presentation markdown into structured data.

Parses enhanced markdown with YAML front-matter and per-slide
<!-- slide: ... --> directives into PresentationModel dataclasses.
Backward-compatible with existing strategy_presentation.md format.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Optional

import yaml
import markdown

from .telegrafen import (
    ALL_LAYOUTS, EXECUTIVE_LAYOUTS, NARRATIVE_LAYOUTS, ALLMOTE_LAYOUTS,
    SHARED_LAYOUTS, PPTX_LAYOUT_MAP,
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class CardSpec:
    icon: str | None = None
    title: str = ""
    body: str = ""
    accent: str | None = None


@dataclass
class ChartSpec:
    chart_type: str = "bar"
    title: str = ""
    data: dict = field(default_factory=dict)
    annotation: str | None = None
    chart_id: str = ""


@dataclass
class SlideModel:
    number: int = 0
    slide_id: str = ""
    title: str = ""
    headline: str = ""
    theme: str = "statement"
    layout: str = "briefing"
    role: str = "main"
    pptx_layout: str = ""
    icon: str | None = None
    transition: str = "none"
    cards: list[CardSpec] = field(default_factory=list)
    charts: list[ChartSpec] = field(default_factory=list)
    macros: list[str] = field(default_factory=list)
    body_md: str = ""
    body_html: str = ""
    speaker_notes: str | None = None
    raw_metadata: dict = field(default_factory=dict)


@dataclass
class PresentationModel:
    title: str = ""
    subtitle: str = ""
    mode: str = "narrative"
    audience: str = "leadership"
    sensitivity: str = "internal"
    date: str = ""
    footer_left: str = "Content-as-Code"
    slides: list[SlideModel] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

_SLIDE_HEADING_RE = re.compile(r"^## (Slide .+)$", re.MULTILINE)
_SLIDE_ID_RE = re.compile(r"Slide\s+(\S+)\s*(?:—|--|-)\s*(.+)")
_SLIDE_META_RE = re.compile(
    r"<!--\s*slide:\s*\n(.*?)\s*-->", re.DOTALL
)
_CHART_META_RE = re.compile(
    r"<!--\s*chart:\s*\n(.*?)\s*-->", re.DOTALL
)
_CARD_META_RE = re.compile(
    r"<!--\s*card:\s*\n(.*?)\s*-->"
    r"(.*?)(?=<!--\s*card:|$)", re.DOTALL
)
_MACRO_RE = re.compile(r"\[\[([A-Z_]+)\]\]")
_HEADLINE_RE = re.compile(
    r"\*\*Headline:\*\*\s*\*(.+?)\*", re.DOTALL
)
_FRONT_MATTER_RE = re.compile(
    r"^---\n(.*?)\n---\n", re.DOTALL
)


def _extract_front_matter(text: str) -> tuple[dict, str]:
    """Extract YAML front-matter and return (metadata, remaining_text)."""
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[m.end():]


def _extract_slide_metadata(body: str) -> tuple[dict, str]:
    """Extract <!-- slide: ... --> YAML block from slide body."""
    m = _SLIDE_META_RE.search(body)
    if not m:
        return {}, body
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    cleaned = body[:m.start()] + body[m.end():]
    return meta, cleaned


def _extract_charts(body: str) -> tuple[list[ChartSpec], str]:
    """Extract <!-- chart: ... --> blocks from slide body."""
    charts = []
    chart_id = 0
    for m in _CHART_META_RE.finditer(body):
        try:
            spec = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        chart_id += 1
        charts.append(ChartSpec(
            chart_type=spec.get("type", "bar"),
            title=spec.get("title", ""),
            data=spec.get("data", {}),
            annotation=spec.get("annotation"),
            chart_id=f"chart_{chart_id}",
        ))
    cleaned = _CHART_META_RE.sub("", body)
    return charts, cleaned


def _extract_cards(body: str) -> tuple[list[CardSpec], str]:
    """Extract <!-- card: ... --> blocks with following body text."""
    cards = []
    for m in _CARD_META_RE.finditer(body):
        try:
            spec = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        card_body = m.group(2).strip()
        cards.append(CardSpec(
            icon=spec.get("icon"),
            title=spec.get("title", ""),
            body=card_body,
            accent=spec.get("accent"),
        ))
    cleaned = _CARD_META_RE.sub("", body)
    return cards, cleaned


def _extract_macros(body: str) -> list[str]:
    """Find all [[MACRO_NAME]] references."""
    return _MACRO_RE.findall(body)


def _extract_headline(body: str) -> tuple[str, str]:
    """Extract **Headline:** *text* pattern."""
    m = _HEADLINE_RE.search(body)
    if not m:
        return "", body
    headline = m.group(1).strip()
    cleaned = body[:m.start()] + body[m.end():]
    return headline, cleaned


def _infer_theme(title: str, body: str, mode: str) -> str:
    """Infer slide theme when no explicit metadata is given."""
    title_lower = title.lower()
    has_preread = any(kw in title_lower for kw in [
        "preread", "background", "deep dive", "appendix", "backup",
    ])
    if has_preread:
        return "light"
    if mode == "executive":
        return "light"
    if mode == "allmote":
        return "statement"
    return "statement"


def _infer_layout(body: str, mode: str, has_cards: bool, has_charts: bool,
                  has_macros: bool, has_table: bool) -> str:
    """Infer slide layout from content when no explicit metadata."""
    if has_cards:
        return "cards-grid"
    if has_charts or has_macros:
        if mode == "executive":
            return "evidence-exhibit"
        if mode == "narrative":
            return "insight-chart"
        return "chart"
    if has_table:
        return "table"
    if mode == "executive":
        return "briefing"
    if mode == "narrative":
        return "story-build"
    return "hero-statement"


def _infer_role(slide_id: str, title: str) -> str:
    """Infer slide role (main, preread, divider, appendix)."""
    title_lower = title.lower()
    if any(c.isalpha() and c != "s" for c in slide_id if not c.isdigit()):
        if "b" in slide_id.lower():
            return "preread"
    if any(kw in title_lower for kw in ["preread", "background", "backup"]):
        return "preread"
    if any(kw in title_lower for kw in ["appendix", "reference"]):
        return "appendix"
    if any(kw in title_lower for kw in ["divider", "section break"]):
        return "divider"
    return "main"


def _md_to_html(md_text: str) -> str:
    """Convert markdown body to HTML."""
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "attr_list"],
    )


def _has_table(body: str) -> bool:
    """Check if body contains a markdown table."""
    lines = body.split("\n")
    for line in lines:
        if re.match(r"\|.*\|.*\|", line):
            return True
    return False


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_presentation(md_path: str, mode_override: str | None = None) -> PresentationModel:
    """Parse a presentation markdown file into a PresentationModel.

    Args:
        md_path: Path to the markdown file
        mode_override: Override the mode from front-matter
    """
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    doc_meta, text = _extract_front_matter(text)

    mode = mode_override or doc_meta.get("mode", "narrative")

    pres = PresentationModel(
        title=doc_meta.get("title", ""),
        subtitle=doc_meta.get("subtitle", ""),
        mode=mode,
        audience=doc_meta.get("audience", "leadership"),
        sensitivity=doc_meta.get("sensitivity", "internal"),
        date=doc_meta.get("date", ""),
        footer_left=doc_meta.get(
            "footer_left",
            "Content-as-Code"
        ),
        metadata=doc_meta,
    )

    parts = _SLIDE_HEADING_RE.split(text)
    # parts[0] is preamble, then pairs of (heading_text, body)

    slide_num = 0
    for i in range(1, len(parts), 2):
        raw_heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""

        # Extract slide ID and title
        id_match = _SLIDE_ID_RE.match(raw_heading)
        if id_match:
            slide_id = id_match.group(1)
            title = id_match.group(2).strip()
        else:
            slide_id = str(slide_num + 1)
            title = raw_heading.replace("Slide ", "").strip()

        slide_num += 1

        # Extract metadata, charts, cards, macros, headline
        slide_meta, body = _extract_slide_metadata(body)
        charts, body = _extract_charts(body)
        cards, body = _extract_cards(body)
        macros = _extract_macros(body)
        headline, body = _extract_headline(body)

        has_table = _has_table(body)

        # Determine theme, layout, role
        theme = slide_meta.get("theme") or _infer_theme(title, body, mode)
        layout = slide_meta.get("layout") or _infer_layout(
            body, mode, bool(cards), bool(charts), bool(macros), has_table
        )
        role = _infer_role(slide_id, title)

        # Determine PPTX layout
        pptx_layout = slide_meta.get("pptx_layout", "")
        if not pptx_layout:
            pptx_layout = PPTX_LAYOUT_MAP.get(layout, "Title and Content")

        # Clean up body — remove visual layout notes
        body = re.sub(
            r">\s*\[!NOTE\].*?(?=\n\n|\n##|\n---|\Z)",
            "",
            body,
            flags=re.DOTALL,
        )
        body = body.strip()

        body_html = _md_to_html(body) if body else ""

        slide = SlideModel(
            number=slide_num,
            slide_id=slide_id,
            title=title,
            headline=headline,
            theme=theme,
            layout=layout,
            role=role,
            pptx_layout=pptx_layout,
            icon=slide_meta.get("icon"),
            transition=slide_meta.get("transition", "none"),
            cards=cards,
            charts=charts,
            macros=macros,
            body_md=body,
            body_html=body_html,
            raw_metadata=slide_meta,
        )

        pres.slides.append(slide)

    # Pair speaker notes: Nb slides attach to slide N
    _pair_speaker_notes(pres.slides)

    return pres


def _pair_speaker_notes(slides: list[SlideModel]) -> None:
    """Link 'Nb' slides as speaker notes for slide 'N'."""
    notes_map: dict[str, int] = {}
    for i, slide in enumerate(slides):
        sid = slide.slide_id.lower()
        if sid.endswith("b") and len(sid) > 1:
            parent_id = sid[:-1]
            notes_map[parent_id] = i

    for slide in slides:
        sid = slide.slide_id.lower()
        if sid in notes_map:
            notes_slide = slides[notes_map[sid]]
            slide.speaker_notes = notes_slide.body_md


def validate_presentation(pres: PresentationModel) -> list[str]:
    """Validate a parsed presentation, returning a list of warnings/errors."""
    issues = []

    mode = pres.mode
    if mode not in ("executive", "narrative", "allmote"):
        issues.append(f"ERROR: Unknown mode '{mode}'. Must be executive, narrative, or allmote.")

    mode_layouts = SHARED_LAYOUTS.copy()
    if mode == "executive":
        mode_layouts |= EXECUTIVE_LAYOUTS
    elif mode == "narrative":
        mode_layouts |= NARRATIVE_LAYOUTS
    elif mode == "allmote":
        mode_layouts |= ALLMOTE_LAYOUTS

    for slide in pres.slides:
        prefix = f"Slide {slide.slide_id}"

        if slide.layout not in ALL_LAYOUTS:
            issues.append(f"ERROR: {prefix}: Unknown layout '{slide.layout}'.")
        elif slide.layout not in mode_layouts:
            issues.append(
                f"WARNING: {prefix}: Layout '{slide.layout}' is not typical "
                f"for mode '{mode}'. Consider a mode-appropriate layout."
            )

        if slide.role == "main" and not slide.title:
            issues.append(f"WARNING: {prefix}: Main slide has no title.")

        if slide.icon:
            from .icon_manager import IconManager
            mgr = IconManager()
            if not mgr.exists(slide.icon):
                issues.append(f"ERROR: {prefix}: Icon '{slide.icon}' not found.")

        for card in slide.cards:
            if card.icon:
                from .icon_manager import IconManager
                mgr = IconManager()
                if not mgr.exists(card.icon):
                    issues.append(
                        f"ERROR: {prefix}: Card icon '{card.icon}' not found."
                    )

    if len(pres.slides) < 3:
        issues.append("WARNING: Presentation has fewer than 3 slides.")
    if len(pres.slides) > 50:
        issues.append("WARNING: Presentation has more than 50 slides.")

    return issues
