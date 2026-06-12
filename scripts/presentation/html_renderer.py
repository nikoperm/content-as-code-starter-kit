"""HTML Renderer — generates interactive fullscreen slide decks from PresentationModel.

Produces a self-contained HTML file with embedded CSS, JS, and Chart.js
support.  Three presentation modes (executive, narrative, allmote) and
29 layout types are supported.  The output works when opened directly
as a file:// URL; fonts and Chart.js load from CDN.

Every layout produces rich, presentation-quality HTML with:
- Glassmorphism headers and footers
- Animated KPI/card components with hover effects
- Dark-blue themed tables with zebra striping
- Professional typography (DM Sans, weight 900 headings)
- Pure CSS bar charts and Chart.js integration
- Scroll-snap fullscreen slides with keyboard navigation
"""

from __future__ import annotations

import html
import os
import re
from typing import List, Optional

from .telegrafen import (
    COLORS,
    CSS_TOKENS,
    PROPELLER_SVG,
    LOGO_SVG_DARK,
    LOGO_SVG_WHITE,
    GOOGLE_FONTS_URL,
    FONT_HEADING,
)
from .slide_parser import PresentationModel, SlideModel, CardSpec, ChartSpec
from .icon_manager import IconManager
from .chart_renderer import render_inline_chart, render_macro, expand_macros_in_html


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ESC = html.escape

# Accent color palette for cards
_ACCENT_COLORS = [
    "var(--tg-telenor-blue)",
    "var(--tg-blue)",
    "#7C3AED",
    "#10B981",
    "var(--tg-accent-pink)",
    "var(--tg-accent-yellow)",
    "var(--tg-accent-green)",
]


def _theme_logo(theme: str) -> str:
    """Return the appropriate logo SVG for a slide theme."""
    return LOGO_SVG_DARK if theme == "light" else LOGO_SVG_WHITE


def _md_table_to_html(text: str) -> str:
    """Convert any remaining raw markdown table lines to proper HTML tables.

    This is a fallback for cases where the markdown library fails to convert
    tables (e.g. when the table is embedded in other HTML or has unusual
    formatting).
    """
    lines = text.split("\n")
    result = []
    in_table = False
    header_done = False

    for line in lines:
        stripped = line.strip()
        # Detect table row: starts and ends with |, has at least 2 | chars
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 3:
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Check if this is a separator row (---|---|---)
            if all(re.match(r"^[-:]+$", c) for c in cells if c):
                if in_table:
                    # This is the header separator, skip it
                    header_done = True
                    continue
                else:
                    continue

            if not in_table:
                result.append('<table class="tg-styled-table">')
                in_table = True
                header_done = False
                # First row is always header
                result.append("<thead><tr>")
                for cell in cells:
                    result.append(f"<th>{cell}</th>")
                result.append("</tr></thead><tbody>")
                continue

            result.append("<tr>")
            for i, cell in enumerate(cells):
                cls = ' class="col-first"' if i == 0 else ""
                result.append(f"<td{cls}>{cell}</td>")
            result.append("</tr>")
        else:
            if in_table:
                result.append("</tbody></table>")
                in_table = False
                header_done = False
            result.append(line)

    if in_table:
        result.append("</tbody></table>")

    return "\n".join(result)


def _post_process_tables(html_str: str) -> str:
    """Post-process HTML to add rich table styling classes.

    Converts plain <table> tags into styled tables with dark-blue headers,
    zebra striping, and proper spacing.
    """
    # Add class to tables that don't have one
    html_str = re.sub(
        r"<table(?!\s+class=)",
        '<table class="tg-styled-table"',
        html_str,
    )
    return html_str


def _post_process_body(body_html: str) -> str:
    """Post-process body HTML to enhance visual quality.

    - Converts remaining markdown tables to HTML
    - Adds rich table styling
    - Wraps standalone lists in styled containers
    """
    if not body_html:
        return ""

    # Check for unconverted markdown tables
    if re.search(r"^\|.*\|.*\|", body_html, re.MULTILINE):
        body_html = _md_table_to_html(body_html)

    # Add rich styling to tables
    body_html = _post_process_tables(body_html)

    return body_html


def _render_slide_header(slide: SlideModel, total: int) -> str:
    """Render the glassmorphism header bar: logo + badge + slide number."""
    logo = _theme_logo(slide.theme)
    if slide.theme == "light":
        badge_bg = "var(--tg-dark-blue)"
        badge_color = "var(--tg-white)"
        header_bg = "rgba(7, 4, 82, 0.95)"
        border_color = "rgba(0, 200, 255, 0.15)"
    elif slide.theme == "statement":
        badge_bg = "rgba(255, 255, 255, 0.12)"
        badge_color = "var(--tg-telenor-blue)"
        header_bg = "rgba(7, 4, 82, 0.6)"
        border_color = "rgba(0, 200, 255, 0.1)"
    else:
        badge_bg = "rgba(255, 255, 255, 0.12)"
        badge_color = "var(--tg-telenor-blue)"
        header_bg = "rgba(0, 0, 0, 0.3)"
        border_color = "rgba(0, 200, 255, 0.08)"

    number_html = ""
    if slide.role in ("main", "preread"):
        number_html = (
            f'<span class="slide-number">{slide.number}</span>'
        )

    return (
        f'<header class="slide-header" style="background:{header_bg};'
        f'border-bottom:1px solid {border_color};backdrop-filter:blur(12px);">'
        f'<div class="header-inner">'
        f'<span class="slide-logo">{logo}</span>'
        f'<span class="slide-badge" style="background:{badge_bg};'
        f'color:{badge_color};">STRATEGY</span>'
        f'{number_html}'
        f'</div>'
        f'</header>'
    )


def _render_slide_footer(
    slide: SlideModel, footer_left: str, index: int, total: int
) -> str:
    """Render glassmorphism footer: left text + propeller + page count."""
    propeller_color = (
        "var(--tg-dark-blue)" if slide.theme == "light" else "var(--tg-telenor-blue)"
    )
    if slide.theme == "light":
        footer_bg = "rgba(7, 4, 82, 0.03)"
        footer_border = "rgba(7, 4, 82, 0.08)"
    else:
        footer_bg = "rgba(0, 0, 0, 0.2)"
        footer_border = "rgba(0, 200, 255, 0.08)"

    return (
        f'<footer class="slide-footer" style="background:{footer_bg};'
        f'border-top:1px solid {footer_border};">'
        f'<span class="footer-text">{_ESC(footer_left)}</span>'
        f'<span class="footer-propeller" style="color:{propeller_color};">'
        f'{PROPELLER_SVG}</span>'
        f'<span class="footer-page">{index + 1} / {total}</span>'
        f'</footer>'
    )


def _render_speaker_notes(slide: SlideModel) -> str:
    """Render hidden speaker notes div."""
    if not slide.speaker_notes:
        return ""
    return (
        f'<div class="speaker-notes" hidden>'
        f'{_ESC(slide.speaker_notes)}'
        f'</div>'
    )


def _render_icon(icon_mgr: IconManager, name: Optional[str], size: int,
                 theme: str) -> str:
    """Safely render an icon; return empty string on failure."""
    if not name:
        return ""
    try:
        return icon_mgr.render_inline(name, size=size, theme=theme)
    except FileNotFoundError:
        return (
            f'<span class="tg-icon-placeholder" style="display:inline-flex;'
            f'align-items:center;justify-content:center;'
            f'width:{size}px;height:{size}px;border-radius:50%;'
            f'background:rgba(0,200,255,0.1);border:1px solid rgba(0,200,255,0.2);'
            f'font-size:{size // 2}px;"></span>'
        )


def _render_cards_html(cards: List[CardSpec], icon_mgr: IconManager,
                       theme: str, mode: str) -> str:
    """Render a list of CardSpec into rich HTML card elements with hover effects."""
    if not cards:
        return ""
    cols = min(len(cards), 4) if mode == "executive" else min(len(cards), 3)
    parts = [f'<div class="tg-cards-grid" style="'
             f'grid-template-columns:repeat({cols},1fr);">']
    icon_size = 36 if mode == "executive" else 56 if mode == "allmote" else 48
    for i, card in enumerate(cards):
        accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
        icon_html = _render_icon(icon_mgr, card.icon, icon_size, theme)
        delay = i * 0.1
        anim_cls = " animate-slide-up" if mode in ("allmote", "narrative") else ""

        parts.append(
            f'<div class="tg-card{anim_cls}" style="'
            f'border-top:4px solid {accent};'
            f'transition-delay:{delay}s;">'
            f'<div class="card-icon-wrap">{icon_html}</div>'
            f'<h4 class="card-title">{_ESC(card.title)}</h4>'
            f'<p class="card-body">{_ESC(card.body)}</p>'
            f'</div>'
        )
    parts.append("</div>")
    return "\n".join(parts)


def _render_charts_html(charts: List[ChartSpec], mode: str) -> str:
    """Render all inline ChartSpec objects."""
    if not charts:
        return ""
    parts = []
    for spec in charts:
        parts.append(render_inline_chart(spec, mode))
    return "\n".join(parts)


def _body_with_macros(slide: SlideModel) -> str:
    """Return body_html with macros expanded and post-processed."""
    if not slide.body_html:
        return ""
    body = expand_macros_in_html(slide.body_html)
    return _post_process_body(body)


# ---------------------------------------------------------------------------
# Layout renderers — each produces rich, styled HTML
# ---------------------------------------------------------------------------

# ---- Executive-only ----

def _render_briefing(slide: SlideModel, mode: str, icon_mgr: IconManager) -> str:
    """Executive briefing: action title, structured body, source footnotes."""
    body = _body_with_macros(slide)
    headline = ""
    if slide.headline:
        headline = (
            f'<div class="briefing-headline">'
            f'<div class="headline-accent"></div>'
            f'<p>{_ESC(slide.headline)}</p>'
            f'</div>'
        )
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)

    return (
        f'<div class="layout-briefing">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{headline}'
        f'<div class="briefing-content">'
        f'<div class="briefing-body rich-content">{body}</div>'
        f'{f"<div class=briefing-charts>{charts_html}</div>" if charts_html else ""}'
        f'</div>'
        f'</div>'
    )


def _render_executive_summary(slide: SlideModel, mode: str,
                              icon_mgr: IconManager) -> str:
    """Executive summary: two-column with findings and actions."""
    body = _body_with_macros(slide)
    cards_html = _render_cards_html(slide.cards, icon_mgr, slide.theme, mode)
    return (
        f'<div class="layout-executive-summary">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="exec-summary-grid">'
        f'<div class="exec-findings">'
        f'<div class="subsection-badge">KEY FINDINGS</div>'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'<div class="exec-actions">'
        f'<div class="subsection-badge accent-green">RECOMMENDED ACTIONS</div>'
        f'{cards_html}'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _render_evidence_exhibit(slide: SlideModel, mode: str,
                             icon_mgr: IconManager) -> str:
    """Evidence exhibit: chart on left, takeaway callout on right."""
    body = _body_with_macros(slide)
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    return (
        f'<div class="layout-evidence-exhibit">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="exhibit-grid">'
        f'<div class="exhibit-chart">{charts_html}</div>'
        f'<div class="exhibit-takeaway">'
        f'<div class="takeaway-box">'
        f'<div class="subsection-badge">KEY TAKEAWAY</div>'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _render_dual_analysis(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Dual analysis: two-column card comparison."""
    body = _body_with_macros(slide)
    cards = slide.cards
    left_cards = cards[: len(cards) // 2] if cards else []
    right_cards = cards[len(cards) // 2:] if cards else []
    return (
        f'<div class="layout-dual-analysis">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="dual-grid">'
        f'<div class="dual-col">'
        f'{_render_cards_html(left_cards, icon_mgr, slide.theme, mode)}'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'<div class="dual-col">'
        f'{_render_cards_html(right_cards, icon_mgr, slide.theme, mode)}'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _render_structured_argument(slide: SlideModel, mode: str,
                                icon_mgr: IconManager) -> str:
    """Structured argument: numbered steps with accent circles."""
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-structured-argument">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="argument-steps rich-content">{body}</div>'
        f'</div>'
    )


def _render_appendix_detail(slide: SlideModel, mode: str,
                            icon_mgr: IconManager) -> str:
    """Appendix detail: badged section with dense content."""
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-appendix-detail">'
        f'<div class="appendix-header">'
        f'<span class="tg-badge appendix-badge">APPENDIX</span>'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="appendix-body rich-content">{body}</div>'
        f'</div>'
    )


# ---- Narrative-only ----

def _render_insight_chart(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Insight chart: visualization on left, callout insight on right."""
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-insight-chart">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="insight-grid">'
        f'<div class="insight-visual">{charts_html}</div>'
        f'<div class="insight-callout">'
        f'<div class="callout-icon">&#x1F4A1;</div>'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _render_story_build(slide: SlideModel, mode: str,
                        icon_mgr: IconManager) -> str:
    """Story build: vertical timeline of connected steps."""
    body = _body_with_macros(slide)
    cards = slide.cards
    if cards:
        steps = []
        for i, card in enumerate(cards):
            icon_html = _render_icon(icon_mgr, card.icon, 40, slide.theme)
            if not icon_html:
                icon_html = f'<span class="step-number">{i + 1}</span>'
            delay = i * 0.15
            accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
            steps.append(
                f'<div class="story-step animate-slide-up" '
                f'style="transition-delay:{delay}s;">'
                f'<div class="story-icon" style="border-color:{accent};">'
                f'{icon_html}'
                f'</div>'
                f'<div class="story-content">'
                f'<strong>{_ESC(card.title)}</strong>'
                f'<p>{_ESC(card.body)}</p>'
                f'</div>'
                f'</div>'
            )
        steps_html = '<div class="story-connector">' + "\n".join(steps) + "</div>"
    else:
        steps_html = f'<div class="rich-content">{body}</div>'

    return (
        f'<div class="layout-story-build">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{steps_html}'
        f'</div>'
    )


def _render_context_split(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Context split: visual on left, rich text on right."""
    body = _body_with_macros(slide)
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    icon_html = _render_icon(icon_mgr, slide.icon, 120, slide.theme)
    visual = charts_html or icon_html
    return (
        f'<div class="layout-context-split">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="context-grid">'
        f'<div class="context-visual">{visual}</div>'
        f'<div class="context-text rich-content">{body}</div>'
        f'</div>'
        f'</div>'
    )


def _render_key_finding(slide: SlideModel, mode: str,
                        icon_mgr: IconManager) -> str:
    """Key finding: bold statement band with supporting evidence below."""
    body = _body_with_macros(slide)
    headline = slide.headline or slide.title
    return (
        f'<div class="layout-key-finding">'
        f'<div class="finding-band">'
        f'<p class="finding-statement">{_ESC(headline)}</p>'
        f'</div>'
        f'<div class="finding-evidence rich-content">{body}</div>'
        f'</div>'
    )


def _render_dashboard(slide: SlideModel, mode: str,
                      icon_mgr: IconManager) -> str:
    """Dashboard: KPI cards grid with large numbers and labels."""
    cards = slide.cards
    body = _body_with_macros(slide)
    cols = min(len(cards), 5) if cards else 3
    kpi_parts = []
    for i, card in enumerate(cards):
        icon_html = _render_icon(icon_mgr, card.icon, 36, slide.theme)
        accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
        delay = i * 0.1
        kpi_parts.append(
            f'<div class="dashboard-kpi animate-slide-up" '
            f'style="border-top:4px solid {accent};transition-delay:{delay}s;">'
            f'<div class="kpi-icon-wrap">{icon_html}</div>'
            f'<span class="kpi-number" data-counter>{_ESC(card.title)}</span>'
            f'<span class="kpi-label">{_ESC(card.body)}</span>'
            f'</div>'
        )
    kpis = (
        f'<div class="dashboard-grid" style="'
        f'grid-template-columns:repeat({cols},1fr);">'
        + "\n".join(kpi_parts)
        + "</div>"
    ) if kpi_parts else ""
    return (
        f'<div class="layout-dashboard">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{kpis}'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
    )


# ---- AllMote-only ----

def _render_hero_statement(slide: SlideModel, mode: str,
                           icon_mgr: IconManager) -> str:
    """Hero statement: giant centered text, cinematic feel."""
    headline = slide.headline or slide.title
    return (
        f'<div class="layout-hero-statement">'
        f'<div class="hero-glow"></div>'
        f'<p class="hero-text animate-fade-in">{_ESC(headline)}</p>'
        f'</div>'
    )


def _render_big_number(slide: SlideModel, mode: str,
                       icon_mgr: IconManager) -> str:
    """Big number: massive counter with annotation below."""
    body_text = re.sub(r'<[^>]+>', '', slide.body_html).strip()
    body_text = body_text.split('\n')[0].strip() if body_text else ''

    number = body_text if body_text else slide.title
    annotation = slide.headline if slide.headline else slide.title
    if number == annotation:
        annotation = ''

    return (
        f'<div class="layout-big-number">'
        f'<div class="big-number-glow"></div>'
        f'<span class="big-num animate-fade-in" data-counter>{_ESC(number)}</span>'
        f'<div class="big-annotation">{_ESC(annotation)}</div>'
        f'</div>'
    )


def _render_icon_showcase(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Icon showcase: large icon centered with text below."""
    icon_html = _render_icon(icon_mgr, slide.icon, 140, slide.theme)
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-icon-showcase">'
        f'<div class="showcase-icon animate-fade-in">{icon_html}</div>'
        f'<div class="showcase-text rich-content">{body}</div>'
        f'</div>'
    )


def _render_animated_reveal(slide: SlideModel, mode: str,
                            icon_mgr: IconManager) -> str:
    """Animated reveal: staggered items that slide in on scroll."""
    cards = slide.cards
    body = _body_with_macros(slide)
    if cards:
        items = []
        for i, card in enumerate(cards):
            delay = i * 0.2
            icon_html = _render_icon(icon_mgr, card.icon, 40, slide.theme)
            accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
            items.append(
                f'<div class="reveal-item animate-slide-up" '
                f'style="transition-delay:{delay}s;border-left:4px solid {accent};">'
                f'<div class="reveal-icon">{icon_html}</div>'
                f'<div class="reveal-content">'
                f'<h4>{_ESC(card.title)}</h4>'
                f'<p>{_ESC(card.body)}</p>'
                f'</div>'
                f'</div>'
            )
        content = "\n".join(items)
    else:
        content = f'<div class="rich-content">{body}</div>'
    return (
        f'<div class="layout-animated-reveal">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="reveal-stack">{content}</div>'
        f'</div>'
    )


def _render_celebration(slide: SlideModel, mode: str,
                        icon_mgr: IconManager) -> str:
    """Celebration: highlighted card with glow effect."""
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-celebration">'
        f'<div class="celebration-card animate-fade-in">'
        f'<div class="celebration-glow"></div>'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'</div>'
    )


def _render_before_after(slide: SlideModel, mode: str,
                         icon_mgr: IconManager) -> str:
    """Before/After: side-by-side comparison with visual contrast."""
    body = _body_with_macros(slide)
    cards = slide.cards
    before_html = ""
    after_html = ""
    if len(cards) >= 2:
        before_html = (
            f'<h3>{_ESC(cards[0].title)}</h3>'
            f'<p>{_ESC(cards[0].body)}</p>'
        )
        after_html = (
            f'<h3>{_ESC(cards[1].title)}</h3>'
            f'<p>{_ESC(cards[1].body)}</p>'
        )
    else:
        before_html = body
    return (
        f'<div class="layout-before-after">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="ba-grid">'
        f'<div class="ba-before animate-slide-up">'
        f'<span class="tg-badge ba-badge-before">BEFORE</span>'
        f'{before_html}'
        f'</div>'
        f'<div class="ba-divider">'
        f'<div class="ba-divider-line"></div>'
        f'<span class="ba-divider-icon">&#x2192;</span>'
        f'<div class="ba-divider-line"></div>'
        f'</div>'
        f'<div class="ba-after animate-slide-up" style="transition-delay:0.2s;">'
        f'<span class="tg-badge ba-badge-after">AFTER</span>'
        f'{after_html}'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _render_photo_impact(slide: SlideModel, mode: str,
                         icon_mgr: IconManager) -> str:
    """Photo impact: full-bleed with glassmorphism overlay."""
    headline = slide.headline or slide.title
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-photo-impact">'
        f'<div class="impact-overlay animate-fade-in">'
        f'<h2 class="impact-text">{_ESC(headline)}</h2>'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
        f'</div>'
    )


# ---- Shared layouts ----

def _render_cards_grid(slide: SlideModel, mode: str,
                       icon_mgr: IconManager) -> str:
    """Card grid: arranged cards with icons, hover effects."""
    body = _body_with_macros(slide)
    return (
        f'<div class="layout-cards-grid">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{_render_cards_html(slide.cards, icon_mgr, slide.theme, mode)}'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
    )


def _render_chart(slide: SlideModel, mode: str,
                  icon_mgr: IconManager) -> str:
    """Chart: dark-blue container with Chart.js and annotation box."""
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    body = _body_with_macros(slide)

    annotation = ""
    if body:
        if mode == "executive":
            annotation = (
                f'<div class="chart-annotation exhibit-style">'
                f'<div class="subsection-badge">ANALYSIS</div>'
                f'{body}'
                f'</div>'
            )
        elif mode == "narrative":
            annotation = (
                f'<div class="chart-annotation insight-style">'
                f'<div class="callout-icon">&#x1F4CA;</div>'
                f'{body}'
                f'</div>'
            )
        else:
            annotation = f'<div class="chart-annotation">{body}</div>'

    return (
        f'<div class="layout-chart">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="chart-content-area">'
        f'{charts_html}'
        f'{annotation}'
        f'</div>'
        f'</div>'
    )


def _render_table(slide: SlideModel, mode: str,
                  icon_mgr: IconManager) -> str:
    """Table: dark-blue header, zebra striping, accent border."""
    body = _body_with_macros(slide)
    density_cls = " table-dense" if mode == "executive" else ""
    return (
        f'<div class="layout-table{density_cls}">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="tg-table-wrap">{body}</div>'
        f'</div>'
    )


def _render_two_column(slide: SlideModel, mode: str,
                       icon_mgr: IconManager) -> str:
    """Two column: flexible split with visual + text."""
    body = _body_with_macros(slide)
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    cards_html = _render_cards_html(slide.cards, icon_mgr, slide.theme, mode)
    left = charts_html or cards_html or ""
    right = body
    return (
        f'<div class="layout-two-column">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="two-col-grid">'
        f'<div class="col-left">{left}</div>'
        f'<div class="col-right rich-content">{right}</div>'
        f'</div>'
        f'</div>'
    )


def _render_three_column(slide: SlideModel, mode: str,
                         icon_mgr: IconManager) -> str:
    """Three column: triple card/content layout."""
    body = _body_with_macros(slide)
    cards_html = _render_cards_html(slide.cards, icon_mgr, slide.theme, mode)
    return (
        f'<div class="layout-three-column">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{cards_html}'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
    )


def _render_numbers_panel(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Numbers panel: grid of large numbers with labels and icons."""
    cards = slide.cards
    body = _body_with_macros(slide)
    cols = min(len(cards), 5) if cards else 3
    items = []
    for i, card in enumerate(cards):
        icon_html = _render_icon(icon_mgr, card.icon, 36, slide.theme)
        accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
        delay = i * 0.12
        items.append(
            f'<div class="number-panel-item animate-slide-up" '
            f'style="transition-delay:{delay}s;border-top:4px solid {accent};">'
            f'<div class="panel-icon">{icon_html}</div>'
            f'<span class="panel-number" data-counter>{_ESC(card.title)}</span>'
            f'<span class="panel-label">{_ESC(card.body)}</span>'
            f'</div>'
        )
    panels = (
        f'<div class="numbers-grid" style="'
        f'grid-template-columns:repeat({cols},1fr);">'
        + "\n".join(items)
        + "</div>"
    ) if items else ""
    return (
        f'<div class="layout-numbers-panel">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{panels}'
        f'<div class="rich-content">{body}</div>'
        f'</div>'
    )


def _render_comparison(slide: SlideModel, mode: str,
                       icon_mgr: IconManager) -> str:
    """Comparison: two-panel side-by-side with visual contrast."""
    body = _body_with_macros(slide)
    cards = slide.cards
    left = ""
    right = ""
    if len(cards) >= 2:
        left = (
            f'<div class="tg-card comparison-card">'
            f'<h4>{_ESC(cards[0].title)}</h4>'
            f'<p>{_ESC(cards[0].body)}</p>'
            f'</div>'
        )
        right = (
            f'<div class="tg-card comparison-card">'
            f'<h4>{_ESC(cards[1].title)}</h4>'
            f'<p>{_ESC(cards[1].body)}</p>'
            f'</div>'
        )
    else:
        left = f'<div class="rich-content">{body}</div>'
    return (
        f'<div class="layout-comparison">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="comparison-grid">'
        f'<div class="comp-left">{left}</div>'
        f'<div class="comp-vs">VS</div>'
        f'<div class="comp-right">{right}</div>'
        f'</div>'
        f'</div>'
    )


def _render_timeline(slide: SlideModel, mode: str,
                     icon_mgr: IconManager) -> str:
    """Timeline: vertical track with connected milestones."""
    body = _body_with_macros(slide)
    cards = slide.cards
    if cards:
        steps = []
        for i, card in enumerate(cards):
            icon_html = _render_icon(icon_mgr, card.icon, 28, slide.theme)
            delay = i * 0.12 if mode != "executive" else 0
            anim_cls = " animate-slide-up" if mode != "executive" else ""
            accent = card.accent or _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
            if not icon_html:
                icon_html = f'<span class="timeline-num">{i + 1}</span>'
            steps.append(
                f'<div class="timeline-step{anim_cls}" '
                f'style="transition-delay:{delay}s;">'
                f'<div class="timeline-dot" style="background:{accent};">'
                f'{icon_html}'
                f'</div>'
                f'<div class="timeline-content">'
                f'<strong>{_ESC(card.title)}</strong>'
                f'<p>{_ESC(card.body)}</p>'
                f'</div>'
                f'</div>'
            )
        content = '<div class="timeline-track">' + "\n".join(steps) + "</div>"
    else:
        content = f'<div class="rich-content">{body}</div>'
    return (
        f'<div class="layout-timeline">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'{content}'
        f'</div>'
    )


def _render_divider(slide: SlideModel, mode: str,
                    icon_mgr: IconManager) -> str:
    """Section divider: centered icon + large text, gradient background."""
    icon_html = _render_icon(icon_mgr, slide.icon, 72, slide.theme)
    headline = slide.headline or slide.title
    return (
        f'<div class="layout-divider">'
        f'<div class="divider-decoration"></div>'
        f'<div class="divider-icon">{icon_html}</div>'
        f'<h2 class="divider-text">{_ESC(headline)}</h2>'
        f'<div class="divider-line"></div>'
        f'</div>'
    )


def _render_title_only(slide: SlideModel, mode: str,
                       icon_mgr: IconManager) -> str:
    """Title only: centered title with optional subtitle, dramatic."""
    headline = slide.headline or slide.title
    body = _body_with_macros(slide)
    subtitle_html = f'<p class="title-subtitle">{body}</p>' if body else ""
    return (
        f'<div class="layout-title-only">'
        f'<div class="title-glow"></div>'
        f'<h1 class="title-main animate-fade-in">{_ESC(headline)}</h1>'
        f'{subtitle_html}'
        f'</div>'
    )


def _render_content_image(slide: SlideModel, mode: str,
                          icon_mgr: IconManager) -> str:
    """Content + image: text on left, visual on right."""
    body = _body_with_macros(slide)
    charts_html = _render_charts_html(slide.charts, mode)
    for macro in slide.macros:
        charts_html += render_macro(macro)
    icon_html = _render_icon(icon_mgr, slide.icon, 100, slide.theme)
    visual = charts_html or icon_html
    return (
        f'<div class="layout-content-image">'
        f'<div class="section-header">'
        f'<h2 class="slide-title">{_ESC(slide.title)}</h2>'
        f'</div>'
        f'<div class="ci-grid">'
        f'<div class="ci-content rich-content">{body}</div>'
        f'<div class="ci-image">{visual}</div>'
        f'</div>'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Layout dispatch table
# ---------------------------------------------------------------------------

_LAYOUT_DISPATCH = {
    # Executive
    "briefing": _render_briefing,
    "executive-summary": _render_executive_summary,
    "evidence-exhibit": _render_evidence_exhibit,
    "dual-analysis": _render_dual_analysis,
    "structured-argument": _render_structured_argument,
    "appendix-detail": _render_appendix_detail,
    # Narrative
    "insight-chart": _render_insight_chart,
    "story-build": _render_story_build,
    "context-split": _render_context_split,
    "key-finding": _render_key_finding,
    "dashboard": _render_dashboard,
    # AllMote
    "hero-statement": _render_hero_statement,
    "big-number": _render_big_number,
    "icon-showcase": _render_icon_showcase,
    "animated-reveal": _render_animated_reveal,
    "celebration": _render_celebration,
    "before-after": _render_before_after,
    "photo-impact": _render_photo_impact,
    # Shared
    "cards-grid": _render_cards_grid,
    "chart": _render_chart,
    "table": _render_table,
    "two-column": _render_two_column,
    "three-column": _render_three_column,
    "numbers-panel": _render_numbers_panel,
    "comparison": _render_comparison,
    "timeline": _render_timeline,
    "divider": _render_divider,
    "title-only": _render_title_only,
    "content-image": _render_content_image,
}


# ---------------------------------------------------------------------------
# CSS — Presentation-quality stylesheet
# ---------------------------------------------------------------------------

def _build_css(mode: str) -> str:
    """Build the complete CSS stylesheet with rich visual components."""
    return f"""
/* ================================================================
   RESET + BASE
   ================================================================ */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}}
body {{
    font-family: var(--tg-font-body);
    scroll-snap-type: y mandatory;
    overflow-y: scroll;
    height: 100vh;
    background: var(--tg-dark-blue);
    color: var(--tg-white);
    line-height: 1.6;
}}

/* ================================================================
   TELEGRAFEN DESIGN TOKENS
   ================================================================ */
{CSS_TOKENS}

/* Extended tokens */
:root {{
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-bounce: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    --shadow-card: 0 10px 30px rgba(7, 4, 82, 0.08);
    --shadow-card-hover: 0 20px 40px rgba(7, 4, 82, 0.15);
    --shadow-glow: 0 0 40px rgba(0, 200, 255, 0.15);
    --glass-bg: rgba(7, 4, 82, 0.6);
    --glass-border: rgba(0, 200, 255, 0.15);
    --glass-blur: blur(12px);
}}

/* ================================================================
   SLIDE CONTAINER
   ================================================================ */
.slide {{
    width: 100vw;
    height: 100vh;
    scroll-snap-align: start;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}}

/* ================================================================
   THEME VARIANTS
   ================================================================ */
.slide-light {{
    background: linear-gradient(180deg, var(--tg-light-cyan) 0%, var(--tg-off-white) 100%);
    color: var(--tg-dark-blue);
}}
.slide-light .slide-title,
.slide-light h2, .slide-light h3, .slide-light h4 {{
    color: var(--tg-dark-blue);
}}
.slide-light .tg-card {{
    background: var(--tg-white);
    color: var(--tg-dark-blue);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(0, 200, 255, 0.1);
}}
.slide-light .tg-card:hover {{
    transform: translateY(-6px);
    box-shadow: var(--shadow-card-hover);
    border-color: var(--tg-telenor-blue);
}}
.slide-light .rich-content {{
    color: var(--tg-dark-blue);
}}

.slide-statement {{
    background: linear-gradient(135deg, var(--tg-dark-blue) 0%, var(--tg-mid-blue) 100%);
    color: #fff;
}}
.slide-statement .tg-card {{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.18);
    color: #fff;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}}
.slide-statement .tg-card:hover {{
    background: rgba(255,255,255,0.18);
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
    border-color: var(--tg-telenor-blue);
}}

.slide-dark {{
    background: var(--tg-dark-blue);
    color: #fff;
}}
.slide-dark .tg-card {{
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    color: #fff;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}}
.slide-dark .tg-card:hover {{
    background: rgba(255,255,255,0.16);
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    border-color: var(--tg-telenor-blue);
}}

/* ================================================================
   MODE VARIANTS — Typography density
   ================================================================ */
.mode-executive {{
    line-height: 1.35;
}}
.mode-executive .rich-content, .mode-executive p {{
    font-size: 0.88rem;
}}
.mode-executive .slide-title {{
    font-size: 1.4rem;
    font-weight: 900;
    letter-spacing: -0.5px;
}}

.mode-narrative {{
    line-height: 1.5;
}}
.mode-narrative .rich-content, .mode-narrative p {{
    font-size: 0.92rem;
}}
.mode-narrative .slide-title {{
    font-size: 1.6rem;
    font-weight: 900;
    letter-spacing: -0.5px;
}}

.mode-allmote {{
    line-height: 1.55;
}}
.mode-allmote .rich-content, .mode-allmote p {{
    font-size: 1rem;
}}
.mode-allmote .slide-title {{
    font-size: 1.8rem;
    font-weight: 900;
    letter-spacing: -0.8px;
}}

/* ================================================================
   GLASSMORPHISM HEADER
   ================================================================ */
.slide-header {{
    display: flex;
    align-items: center;
    padding: 0;
    flex-shrink: 0;
    z-index: 10;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.header-inner {{
    display: flex;
    align-items: center;
    gap: var(--tg-space-sm);
    padding: 10px var(--tg-space-lg);
    width: 100%;
}}
.slide-logo svg {{
    width: 20px;
    height: 20px;
    opacity: 0.8;
}}
.slide-badge {{
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.62rem;
    font-weight: 800;
    border-radius: var(--tg-radius-pill);
    padding: 4px 14px;
}}
.slide-number {{
    margin-left: auto;
    font-size: 0.72rem;
    font-weight: 700;
    opacity: 0.7;
    background: rgba(255,255,255,0.08);
    padding: 3px 10px;
    border-radius: var(--tg-radius-sm);
}}
.slide-light .slide-number {{
    background: rgba(7,4,82,0.06);
    color: var(--tg-dark-blue);
}}

/* ================================================================
   GLASSMORPHISM FOOTER
   ================================================================ */
.slide-footer {{
    display: flex;
    align-items: center;
    gap: var(--tg-space-sm);
    padding: 8px var(--tg-space-lg);
    flex-shrink: 0;
    margin-top: auto;
    font-size: 0.68rem;
    opacity: 0.6;
    z-index: 10;
    backdrop-filter: blur(4px);
}}
.footer-text {{
    flex: 1;
    letter-spacing: 0.02em;
}}
.footer-logo {{
    width: 18px;
    height: 18px;
}}
.footer-propeller svg {{
    width: 18px;
    height: 18px;
}}
.footer-page {{
    font-weight: 700;
    font-size: 0.72rem;
}}

/* ================================================================
   SECTION HEADER — Accent border left
   ================================================================ */
.section-header {{
    border-left: 5px solid var(--tg-telenor-blue);
    padding-left: var(--tg-space-sm);
    margin-bottom: var(--tg-space-md);
}}
.slide-light .section-header {{
    border-left-color: var(--tg-blue);
}}
.slide-title {{
    font-family: var(--tg-font-heading);
    font-weight: 900;
    line-height: 1.2;
    letter-spacing: -0.5px;
}}

/* ================================================================
   RICH CONTENT — Enhanced body text
   ================================================================ */
.rich-content h3 {{
    font-size: 1rem;
    font-weight: 800;
    margin: var(--tg-space-sm) 0 var(--tg-space-xs);
    color: var(--tg-telenor-blue);
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}
.slide-light .rich-content h3 {{
    color: var(--tg-mid-blue);
}}
.rich-content h4 {{
    font-size: 0.92rem;
    font-weight: 700;
    margin: var(--tg-space-xs) 0 4px;
}}
.rich-content ul, .rich-content ol {{
    padding-left: 1.5em;
    margin-bottom: var(--tg-space-sm);
}}
.rich-content li {{
    margin-bottom: 6px;
    line-height: 1.5;
    position: relative;
}}
.rich-content li::marker {{
    color: var(--tg-telenor-blue);
}}
.slide-light .rich-content li::marker {{
    color: var(--tg-blue);
}}
.rich-content strong {{
    font-weight: 800;
}}
.rich-content blockquote {{
    border-left: 3px solid var(--tg-telenor-blue);
    padding: var(--tg-space-xs) var(--tg-space-sm);
    margin: var(--tg-space-sm) 0;
    background: rgba(0,200,255,0.05);
    border-radius: 0 var(--tg-radius-sm) var(--tg-radius-sm) 0;
    font-style: italic;
    opacity: 0.9;
}}
.rich-content a {{
    color: var(--tg-telenor-blue);
    text-decoration: none;
    border-bottom: 1px solid rgba(0,200,255,0.3);
    transition: var(--transition-smooth);
}}
.rich-content a:hover {{
    border-bottom-color: var(--tg-telenor-blue);
}}
.slide-light .rich-content a {{
    color: var(--tg-mid-blue);
    border-bottom-color: rgba(28,22,197,0.2);
}}
.rich-content code {{
    font-family: var(--tg-font-mono);
    background: rgba(255,255,255,0.1);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.82em;
}}
.slide-light .rich-content code {{
    background: rgba(7,4,82,0.06);
}}
.rich-content p {{
    margin-bottom: var(--tg-space-xs);
}}

/* ================================================================
   SUBSECTION BADGES
   ================================================================ */
.subsection-badge {{
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: var(--tg-radius-pill);
    margin-bottom: var(--tg-space-sm);
    background: rgba(0, 200, 255, 0.1);
    color: var(--tg-telenor-blue);
    border: 1px solid rgba(0, 200, 255, 0.2);
}}
.subsection-badge.accent-green {{
    background: rgba(0, 210, 138, 0.1);
    color: var(--tg-success);
    border-color: rgba(0, 210, 138, 0.2);
}}
.slide-light .subsection-badge {{
    background: rgba(7, 4, 82, 0.06);
    color: var(--tg-mid-blue);
    border-color: rgba(7, 4, 82, 0.1);
}}

/* ================================================================
   CARDS — Glassmorphism card component
   ================================================================ */
.layout-cards-grid {{
    justify-content: center;
}}
.tg-cards-grid {{
    display: grid;
    gap: var(--tg-space-lg);
    align-content: center;
}}
.tg-card {{
    background: rgba(255,255,255,0.08);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-lg) var(--tg-space-md) var(--tg-space-md);
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}}
.tg-card::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: var(--tg-telenor-blue);
    transform: scaleX(0);
    transition: transform 0.3s ease;
    transform-origin: left;
}}
.tg-card:hover::after {{
    transform: scaleX(1);
}}
.card-icon-wrap {{
    margin-bottom: var(--tg-space-xs);
    display: flex;
    align-items: center;
}}
.card-title {{
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 8px;
    line-height: 1.3;
    letter-spacing: -0.3px;
}}
.card-body {{
    font-size: 0.88rem;
    opacity: 0.75;
    line-height: 1.55;
}}
.mode-allmote .card-title {{
    font-size: 1.25rem;
}}
.mode-allmote .card-body {{
    font-size: 0.95rem;
}}

/* ================================================================
   TABLES — Dark-blue header, zebra striping, accent border
   ================================================================ */
.tg-table-wrap {{
    overflow-x: auto;
    border-radius: var(--tg-radius-md);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(0, 200, 255, 0.1);
}}
.tg-table-wrap table,
.tg-styled-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    line-height: 1.5;
}}
.tg-table-wrap th,
.tg-styled-table th {{
    background: var(--tg-dark-blue);
    color: var(--tg-white);
    padding: 12px 16px;
    text-align: left;
    font-weight: 800;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
    border-bottom: 2px solid var(--tg-telenor-blue);
}}
.tg-table-wrap td,
.tg-styled-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0, 200, 255, 0.08);
    vertical-align: top;
}}
.tg-table-wrap tr:nth-child(even) td,
.tg-styled-table tr:nth-child(even) td {{
    background: rgba(0, 200, 255, 0.03);
}}
.tg-table-wrap tr:hover td,
.tg-styled-table tr:hover td {{
    background: rgba(0, 200, 255, 0.06);
}}
.tg-table-wrap td:first-child,
.tg-styled-table td:first-child,
.tg-styled-table .col-first {{
    font-weight: 700;
}}

/* Light theme table overrides */
.slide-light .tg-table-wrap {{
    border-color: rgba(7, 4, 82, 0.08);
}}
.slide-light .tg-table-wrap td,
.slide-light .tg-styled-table td {{
    border-bottom-color: rgba(7, 4, 82, 0.06);
    color: var(--tg-dark-blue);
}}
.slide-light .tg-table-wrap tr:nth-child(even) td,
.slide-light .tg-styled-table tr:nth-child(even) td {{
    background: rgba(7, 4, 82, 0.02);
}}
.slide-light .tg-table-wrap tr:hover td,
.slide-light .tg-styled-table tr:hover td {{
    background: rgba(7, 4, 82, 0.04);
}}

/* Dense table (executive mode) */
.table-dense .tg-table-wrap td,
.table-dense .tg-table-wrap th {{
    padding: 6px 10px;
    font-size: 0.72rem;
}}

/* ================================================================
   CHART CONTAINER
   ================================================================ */
.tg-chart-container {{
    background: linear-gradient(135deg, rgba(7,4,82,0.95) 0%, rgba(28,22,197,0.3) 100%);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-md);
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(7, 4, 82, 0.15);
    border: 1px solid rgba(0, 200, 255, 0.08);
}}
.tg-chart-container::before {{
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(0, 200, 255, 0.04) 0%, transparent 70%);
    pointer-events: none;
}}
.slide-light .tg-chart-container {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
    border-color: rgba(0, 200, 255, 0.1);
}}

/* Chart annotation boxes */
.chart-annotation {{
    margin-top: var(--tg-space-sm);
    padding: var(--tg-space-sm) var(--tg-space-md);
    border-radius: var(--tg-radius-md);
    font-size: 0.85rem;
}}
.chart-annotation.exhibit-style {{
    background: rgba(255,255,255,0.06);
    border-left: 4px solid var(--tg-telenor-blue);
}}
.chart-annotation.insight-style {{
    background: rgba(0,200,255,0.06);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: var(--tg-radius-md);
    display: flex;
    gap: var(--tg-space-sm);
    align-items: flex-start;
}}
.slide-light .chart-annotation.exhibit-style {{
    background: var(--tg-off-white);
}}
.slide-light .chart-annotation.insight-style {{
    background: rgba(7,4,82,0.03);
    border-color: rgba(7,4,82,0.08);
}}

/* ================================================================
   BADGE COMPONENT
   ================================================================ */
.tg-badge {{
    display: inline-block;
    background: var(--tg-telenor-blue);
    color: var(--tg-dark-blue);
    font-size: 0.62rem;
    font-weight: 800;
    padding: 3px 14px;
    border-radius: var(--tg-radius-pill);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

/* ================================================================
   COMMON LAYOUT SCAFFOLDING
   ================================================================ */
.slide > [class^="layout-"] {{
    flex: 1;
    padding: var(--tg-space-lg) var(--tg-space-2xl) var(--tg-space-md);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    scrollbar-width: thin;
}}

/* ================================================================
   LAYOUT: BRIEFING
   ================================================================ */
.briefing-headline {{
    display: flex;
    align-items: center;
    gap: var(--tg-space-sm);
    margin-bottom: var(--tg-space-md);
    padding: var(--tg-space-xs) var(--tg-space-sm);
    background: rgba(0,200,255,0.05);
    border-radius: var(--tg-radius-sm);
    border-left: 3px solid var(--tg-telenor-blue);
}}
.briefing-headline p {{
    font-size: 1.05rem;
    font-weight: 600;
    font-style: italic;
    opacity: 0.85;
}}
.slide-light .briefing-headline {{
    background: rgba(7,4,82,0.03);
    border-left-color: var(--tg-blue);
}}
.briefing-content {{
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: var(--tg-space-sm);
}}
.briefing-body {{
    flex: 1;
}}
.briefing-charts {{
    margin-top: auto;
}}

/* ================================================================
   LAYOUT: EXECUTIVE SUMMARY
   ================================================================ */
.exec-summary-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
}}
.exec-findings, .exec-actions {{
    overflow-y: auto;
    padding: var(--tg-space-sm);
    background: rgba(255,255,255,0.03);
    border-radius: var(--tg-radius-md);
}}
.slide-light .exec-findings,
.slide-light .exec-actions {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(0,200,255,0.08);
}}

/* ================================================================
   LAYOUT: EVIDENCE EXHIBIT
   ================================================================ */
.exhibit-grid {{
    display: grid;
    grid-template-columns: 60% 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
    align-items: start;
}}
.takeaway-box {{
    background: rgba(0,200,255,0.06);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: var(--tg-radius-md);
    padding: var(--tg-space-md);
}}
.slide-light .takeaway-box {{
    background: var(--tg-white);
    border-color: rgba(7,4,82,0.08);
    box-shadow: var(--shadow-card);
}}

/* ================================================================
   LAYOUT: DUAL ANALYSIS
   ================================================================ */
.dual-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
}}
.dual-col {{
    display: flex;
    flex-direction: column;
    gap: var(--tg-space-sm);
}}

/* ================================================================
   LAYOUT: STRUCTURED ARGUMENT
   ================================================================ */
.argument-steps {{
    flex: 1;
    counter-reset: arg-step;
}}
.argument-steps li {{
    position: relative;
    padding-left: var(--tg-space-xl);
}}
.argument-steps ol {{
    list-style: none;
    padding: 0;
}}
.argument-steps ol li {{
    counter-increment: arg-step;
    margin-bottom: var(--tg-space-md);
    padding: var(--tg-space-sm);
    background: rgba(255,255,255,0.04);
    border-radius: var(--tg-radius-md);
    border-left: 3px solid var(--tg-telenor-blue);
    transition: var(--transition-smooth);
}}
.argument-steps ol li:hover {{
    background: rgba(255,255,255,0.08);
    transform: translateX(4px);
}}
.argument-steps ol li::before {{
    content: counter(arg-step);
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--tg-telenor-blue);
    color: var(--tg-dark-blue);
    font-weight: 900;
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.slide-light .argument-steps ol li {{
    background: var(--tg-white);
    box-shadow: 0 2px 8px rgba(7,4,82,0.04);
    border-left-color: var(--tg-blue);
}}

/* ================================================================
   LAYOUT: APPENDIX DETAIL
   ================================================================ */
.appendix-header {{
    display: flex;
    align-items: center;
    gap: var(--tg-space-sm);
    margin-bottom: var(--tg-space-sm);
    border-left: 5px solid var(--tg-text-muted);
    padding-left: var(--tg-space-sm);
}}
.appendix-badge {{
    background: var(--tg-text-muted);
    color: var(--tg-white);
}}
.appendix-body {{
    flex: 1;
    overflow-y: auto;
    font-size: 0.78rem;
}}

/* ================================================================
   LAYOUT: INSIGHT CHART
   ================================================================ */
.insight-grid {{
    display: grid;
    grid-template-columns: 55% 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
    align-items: start;
}}
.insight-callout {{
    background: rgba(0,200,255,0.06);
    border: 1px solid rgba(0,200,255,0.15);
    border-left: 4px solid var(--tg-telenor-blue);
    border-radius: var(--tg-radius-md);
    padding: var(--tg-space-md);
    font-size: 0.9rem;
    line-height: 1.6;
}}
.callout-icon {{
    font-size: 1.5rem;
    margin-bottom: var(--tg-space-xs);
}}
.slide-light .insight-callout {{
    background: var(--tg-white);
    border-color: rgba(7,4,82,0.08);
    border-left-color: var(--tg-blue);
    box-shadow: var(--shadow-card);
}}

/* ================================================================
   LAYOUT: STORY BUILD
   ================================================================ */
.story-connector {{
    position: relative;
    padding-left: var(--tg-space-xl);
    flex: 1;
}}
.story-connector::before {{
    content: '';
    position: absolute;
    left: 19px;
    top: 10px;
    bottom: 10px;
    width: 3px;
    background: linear-gradient(180deg, var(--tg-telenor-blue), var(--tg-mid-blue));
    border-radius: 2px;
    opacity: 0.4;
}}
.story-step {{
    display: flex;
    gap: var(--tg-space-md);
    margin-bottom: var(--tg-space-md);
    align-items: flex-start;
    padding: var(--tg-space-sm);
    background: rgba(255,255,255,0.04);
    border-radius: var(--tg-radius-md);
    transition: var(--transition-smooth);
}}
.story-step:hover {{
    background: rgba(255,255,255,0.08);
    transform: translateX(6px);
}}
.slide-light .story-step {{
    background: var(--tg-white);
    box-shadow: 0 2px 8px rgba(7,4,82,0.04);
}}
.slide-light .story-step:hover {{
    box-shadow: var(--shadow-card);
}}
.story-icon {{
    flex-shrink: 0;
    z-index: 1;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--tg-telenor-blue);
    background: rgba(0,200,255,0.05);
}}
.step-number {{
    font-weight: 900;
    font-size: 1rem;
    color: var(--tg-telenor-blue);
}}
.story-content strong {{
    display: block;
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 4px;
}}
.story-content p {{
    font-size: 0.85rem;
    opacity: 0.8;
    line-height: 1.5;
}}

/* ================================================================
   LAYOUT: CONTEXT SPLIT
   ================================================================ */
.context-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
    align-items: center;
}}
.context-visual {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
}}

/* ================================================================
   LAYOUT: KEY FINDING
   ================================================================ */
.layout-key-finding {{
    gap: var(--tg-space-md);
}}
.finding-band {{
    background: linear-gradient(135deg, var(--tg-telenor-blue) 0%, var(--tg-blue) 100%);
    color: var(--tg-dark-blue);
    padding: var(--tg-space-xl) var(--tg-space-2xl);
    border-radius: var(--tg-radius-lg);
    box-shadow: 0 10px 30px rgba(0,200,255,0.2);
    position: relative;
    overflow: hidden;
}}
.finding-band::before {{
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    pointer-events: none;
}}
.finding-statement {{
    font-size: 2.2rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    line-height: 1.15;
    letter-spacing: -1px;
}}
.finding-evidence {{
    background: rgba(255,255,255,0.06);
    border-radius: var(--tg-radius-md);
    padding: var(--tg-space-md) var(--tg-space-lg);
    flex: 1;
    overflow-y: auto;
    border: 1px solid rgba(255,255,255,0.08);
}}
.slide-light .finding-evidence {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
    border-color: rgba(0,200,255,0.1);
}}

/* ================================================================
   LAYOUT: DASHBOARD
   ================================================================ */
.dashboard-grid {{
    display: grid;
    gap: var(--tg-space-md);
    margin-bottom: var(--tg-space-sm);
}}
.dashboard-kpi {{
    background: rgba(255,255,255,0.06);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-md);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--tg-space-xs);
    transition: var(--transition-smooth);
    border: 1px solid rgba(255,255,255,0.06);
}}
.dashboard-kpi:hover {{
    transform: translateY(-6px);
    box-shadow: var(--shadow-glow);
    border-color: var(--tg-telenor-blue);
}}
.slide-light .dashboard-kpi {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(0,200,255,0.1);
}}
.slide-light .dashboard-kpi:hover {{
    box-shadow: var(--shadow-card-hover);
}}
.kpi-icon-wrap {{
    margin-bottom: 4px;
}}
.kpi-number {{
    font-size: 2.8rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    color: var(--tg-telenor-blue);
    line-height: 1;
    letter-spacing: -1px;
}}
.slide-light .kpi-number {{
    color: var(--tg-mid-blue);
}}
.kpi-label {{
    font-size: 0.78rem;
    opacity: 0.6;
    font-weight: 600;
}}

/* ================================================================
   LAYOUT: HERO STATEMENT (AllMote)
   ================================================================ */
.layout-hero-statement {{
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 10vh 8vw;
    position: relative;
    overflow: hidden;
}}
.hero-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,255,0.12) 0%, rgba(0,200,255,0.03) 40%, transparent 70%);
    pointer-events: none;
    animation: pulse-glow-bg 4s ease-in-out infinite alternate;
}}
.hero-text {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 900;
    font-family: var(--tg-font-heading);
    line-height: 1.15;
    letter-spacing: -2px;
    max-width: 75%;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 40px rgba(0,0,0,0.3);
}}
.slide-dark .hero-text {{
    color: var(--tg-white);
}}
.slide-statement .hero-text {{
    text-shadow: 0 4px 30px rgba(0,0,0,0.4);
}}

/* ================================================================
   LAYOUT: BIG NUMBER (AllMote)
   ================================================================ */
.layout-big-number {{
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
    padding: 10vh 8vw;
    overflow: hidden;
}}
.big-number-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,255,0.10) 0%, rgba(0,200,255,0.02) 50%, transparent 70%);
    pointer-events: none;
    animation: pulse-glow-bg 5s ease-in-out infinite alternate;
}}
.big-num {{
    font-size: clamp(5rem, 12vw, 9rem);
    font-weight: 900;
    font-family: var(--tg-font-heading);
    color: var(--tg-telenor-blue);
    line-height: 1;
    letter-spacing: -4px;
    position: relative;
    z-index: 1;
    text-shadow: 0 0 60px rgba(0,200,255,0.25), 0 0 120px rgba(0,200,255,0.1);
}}
.big-annotation {{
    font-size: 1.2rem;
    margin-top: var(--tg-space-lg);
    opacity: 0.6;
    max-width: 50%;
    line-height: 1.5;
    font-weight: 500;
    letter-spacing: 0.02em;
}}

/* ================================================================
   LAYOUT: ICON SHOWCASE (AllMote)
   ================================================================ */
.layout-icon-showcase {{
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: var(--tg-space-lg);
}}
.showcase-icon {{
    transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}}
.showcase-icon.visible {{
    transform: scale(1);
}}
.showcase-text {{
    font-size: 1.15rem;
    max-width: 55%;
    opacity: 0.85;
    line-height: 1.6;
}}

/* ================================================================
   LAYOUT: ANIMATED REVEAL (AllMote)
   ================================================================ */
.reveal-stack {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--tg-space-sm);
    justify-content: center;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
}}
.reveal-item {{
    display: flex;
    align-items: center;
    gap: var(--tg-space-md);
    padding: var(--tg-space-sm) var(--tg-space-md);
    background: rgba(255,255,255,0.06);
    border-radius: var(--tg-radius-md);
    transition: var(--transition-smooth);
}}
.reveal-item:hover {{
    background: rgba(255,255,255,0.1);
    transform: translateX(8px);
}}
.slide-light .reveal-item {{
    background: var(--tg-white);
    box-shadow: 0 2px 8px rgba(7,4,82,0.04);
}}
.reveal-icon {{
    flex-shrink: 0;
}}
.reveal-content h4 {{
    margin: 0 0 4px;
    font-size: 1rem;
    font-weight: 800;
}}
.reveal-content p {{
    margin: 0;
    font-size: 0.85rem;
    opacity: 0.8;
}}

/* ================================================================
   LAYOUT: CELEBRATION (AllMote)
   ================================================================ */
.layout-celebration {{
    justify-content: center;
    align-items: center;
    padding: var(--tg-space-xl);
}}
.celebration-card {{
    background: rgba(255,255,255,0.08);
    border: 2px solid var(--tg-win-green);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-xl) var(--tg-space-2xl);
    text-align: center;
    max-width: 65%;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(0,135,90,0.12);
}}
.celebration-glow {{
    position: absolute;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,135,90,0.08) 0%, transparent 70%);
    pointer-events: none;
}}
.celebration-card .slide-title {{
    color: var(--tg-accent4);
    font-size: 1.8rem;
    margin-bottom: var(--tg-space-sm);
}}

/* ================================================================
   LAYOUT: BEFORE/AFTER (AllMote)
   ================================================================ */
.ba-grid {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--tg-space-md);
    flex: 1;
    align-items: stretch;
}}
.ba-before {{
    background: rgba(255,255,255,0.04);
    border-radius: var(--tg-radius-md);
    padding: var(--tg-space-lg);
    opacity: 0.7;
    filter: saturate(0.4);
    border: 1px solid rgba(255,255,255,0.08);
    transition: var(--transition-smooth);
}}
.ba-before:hover {{
    opacity: 0.85;
}}
.ba-after {{
    background: rgba(0,200,255,0.06);
    border-radius: var(--tg-radius-md);
    padding: var(--tg-space-lg);
    border: 2px solid var(--tg-telenor-blue);
    box-shadow: var(--shadow-glow);
    transition: var(--transition-smooth);
}}
.ba-divider {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--tg-space-xs);
    padding: 0 var(--tg-space-xs);
}}
.ba-divider-line {{
    width: 2px;
    flex: 1;
    background: rgba(0,200,255,0.2);
    border-radius: 1px;
}}
.ba-divider-icon {{
    font-size: 1.5rem;
    color: var(--tg-telenor-blue);
    font-weight: 900;
}}
.ba-badge-before {{
    background: var(--tg-text-muted);
    color: var(--tg-white);
    margin-bottom: var(--tg-space-sm);
}}
.ba-badge-after {{
    background: var(--tg-telenor-blue);
    color: var(--tg-dark-blue);
    margin-bottom: var(--tg-space-sm);
}}

/* ================================================================
   LAYOUT: PHOTO IMPACT (AllMote)
   ================================================================ */
.layout-photo-impact {{
    justify-content: center;
    align-items: center;
    padding: var(--tg-space-xl);
    position: relative;
}}
.impact-overlay {{
    background: rgba(7,4,82,0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,200,255,0.1);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-xl) var(--tg-space-2xl);
    text-align: center;
    max-width: 75%;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}}
.impact-text {{
    font-size: 2.5rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    margin-bottom: var(--tg-space-md);
    line-height: 1.15;
    letter-spacing: -1px;
}}

/* ================================================================
   LAYOUT: TWO COLUMN
   ================================================================ */
.two-col-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
}}
.col-left, .col-right {{
    display: flex;
    flex-direction: column;
    gap: var(--tg-space-sm);
}}

/* ================================================================
   LAYOUT: THREE COLUMN
   ================================================================ */
.layout-three-column .tg-cards-grid {{
    grid-template-columns: repeat(3, 1fr) !important;
}}

/* ================================================================
   LAYOUT: NUMBERS PANEL
   ================================================================ */
.numbers-grid {{
    display: grid;
    gap: var(--tg-space-md);
    margin-bottom: var(--tg-space-sm);
}}
.number-panel-item {{
    background: rgba(255,255,255,0.06);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-md);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--tg-space-xs);
    transition: var(--transition-smooth);
    border: 1px solid rgba(255,255,255,0.06);
}}
.number-panel-item:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow);
    border-color: rgba(0,200,255,0.2);
}}
.slide-light .number-panel-item {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
    border-color: rgba(0,200,255,0.1);
}}
.panel-icon {{
    margin-bottom: 4px;
}}
.panel-number {{
    font-size: 2.2rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    color: var(--tg-telenor-blue);
    line-height: 1;
    letter-spacing: -1px;
}}
.slide-light .panel-number {{
    color: var(--tg-mid-blue);
}}
.panel-label {{
    font-size: 0.78rem;
    opacity: 0.6;
    font-weight: 600;
}}

/* ================================================================
   LAYOUT: COMPARISON
   ================================================================ */
.comparison-grid {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--tg-space-md);
    flex: 1;
    align-items: center;
}}
.comparison-card {{
    padding: var(--tg-space-lg);
}}
.comparison-card h4 {{
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: var(--tg-space-sm);
}}
.comp-vs {{
    font-size: 1.2rem;
    font-weight: 900;
    color: var(--tg-telenor-blue);
    background: rgba(0,200,255,0.1);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgba(0,200,255,0.3);
}}

/* ================================================================
   LAYOUT: TIMELINE
   ================================================================ */
.timeline-track {{
    position: relative;
    padding-left: var(--tg-space-xl);
    flex: 1;
}}
.timeline-track::before {{
    content: '';
    position: absolute;
    left: 14px;
    top: 5px;
    bottom: 5px;
    width: 3px;
    background: linear-gradient(180deg, var(--tg-telenor-blue), var(--tg-mid-blue), var(--tg-blue));
    border-radius: 2px;
    opacity: 0.5;
}}
.timeline-step {{
    display: flex;
    gap: var(--tg-space-md);
    margin-bottom: var(--tg-space-md);
    align-items: flex-start;
    padding: var(--tg-space-xs) 0;
    transition: var(--transition-smooth);
}}
.timeline-step:hover {{
    transform: translateX(6px);
}}
.timeline-dot {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--tg-telenor-blue);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    z-index: 1;
    box-shadow: 0 0 12px rgba(0,200,255,0.3);
}}
.timeline-num {{
    font-size: 0.72rem;
    font-weight: 900;
    color: var(--tg-dark-blue);
}}
.timeline-content {{
    padding-top: 4px;
}}
.timeline-content strong {{
    display: block;
    margin-bottom: 4px;
    font-weight: 800;
}}
.timeline-content p {{
    font-size: 0.85rem;
    opacity: 0.8;
}}

/* ================================================================
   LAYOUT: DIVIDER
   ================================================================ */
.layout-divider {{
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: var(--tg-space-md);
    position: relative;
}}
.divider-decoration {{
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}}
.divider-icon {{
    position: relative;
    z-index: 1;
}}
.divider-text {{
    font-size: 2.4rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    letter-spacing: -1px;
    line-height: 1.2;
    position: relative;
    z-index: 1;
}}
.divider-line {{
    width: 60px;
    height: 4px;
    background: var(--tg-telenor-blue);
    border-radius: 2px;
    margin-top: var(--tg-space-xs);
}}

/* ================================================================
   LAYOUT: TITLE ONLY
   ================================================================ */
.layout-title-only {{
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: var(--tg-space-sm);
    position: relative;
}}
.title-glow {{
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}}
.title-main {{
    font-size: 3rem;
    font-weight: 900;
    font-family: var(--tg-font-heading);
    line-height: 1.12;
    letter-spacing: -1.5px;
    position: relative;
    z-index: 1;
}}
.title-subtitle {{
    font-size: 1.15rem;
    opacity: 0.7;
    max-width: 60%;
    line-height: 1.5;
    position: relative;
    z-index: 1;
}}

/* ================================================================
   LAYOUT: CONTENT IMAGE
   ================================================================ */
.ci-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--tg-space-lg);
    flex: 1;
    align-items: center;
}}
.ci-image {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    background: rgba(255,255,255,0.03);
    border-radius: var(--tg-radius-lg);
    padding: var(--tg-space-md);
}}
.slide-light .ci-image {{
    background: var(--tg-white);
    box-shadow: var(--shadow-card);
}}

/* ================================================================
   LAYOUT: TABLE (additional)
   ================================================================ */
.chart-content-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--tg-space-sm);
}}

/* ================================================================
   INTERACTIVE: Progress bar
   ================================================================ */
.progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--tg-telenor-blue), var(--tg-blue));
    z-index: 1000;
    transition: width 0.3s ease;
    box-shadow: 0 0 8px rgba(0,200,255,0.4);
}}

/* ================================================================
   INTERACTIVE: Slide counter
   ================================================================ */
.slide-counter {{
    position: fixed;
    bottom: var(--tg-space-sm);
    right: var(--tg-space-sm);
    background: rgba(7,4,82,0.9);
    color: var(--tg-telenor-blue);
    font-size: 0.72rem;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: var(--tg-radius-sm);
    z-index: 1000;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,200,255,0.15);
    letter-spacing: 0.05em;
}}

/* ================================================================
   INTERACTIVE: Notes drawer
   ================================================================ */
.notes-drawer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 40vh;
    background: rgba(7,4,82,0.95);
    color: var(--tg-white);
    padding: var(--tg-space-md) var(--tg-space-lg);
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 999;
    overflow-y: auto;
    border-top: 2px solid var(--tg-telenor-blue);
    backdrop-filter: blur(12px);
    font-size: 0.88rem;
    line-height: 1.6;
}}
.notes-drawer.open {{
    transform: translateY(0);
}}
.notes-drawer h4 {{
    color: var(--tg-telenor-blue);
    margin-bottom: var(--tg-space-xs);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 800;
}}

/* ================================================================
   ANIMATIONS
   ================================================================ */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes pulse-glow-bg {{
    from {{ opacity: 0.5; transform: scale(0.9); }}
    to {{ opacity: 1; transform: scale(1.1); }}
}}

@keyframes shine {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* Scoped animations — only for narrative/allmote modes */
.mode-narrative .animate-fade-in,
.mode-allmote .animate-fade-in {{
    opacity: 0;
    transition: opacity 0.6s ease, transform 0.6s ease;
    transform: translateY(15px);
}}
.mode-narrative .animate-fade-in.visible,
.mode-allmote .animate-fade-in.visible {{
    opacity: 1;
    transform: translateY(0);
}}
.mode-narrative .animate-slide-up,
.mode-allmote .animate-slide-up {{
    transform: translateY(30px);
    opacity: 0;
    transition: transform 0.5s ease, opacity 0.5s ease;
}}
.mode-narrative .animate-slide-up.visible,
.mode-allmote .animate-slide-up.visible {{
    transform: translateY(0);
    opacity: 1;
}}

/* Counter animation support */
.animate-counter {{
    transition: all 0.8s ease-out;
}}

/* Spin utility */
.spin {{
    animation: spin 3s linear infinite;
}}

/* ================================================================
   PRINT / PDF
   ================================================================ */
@media print {{
    body {{
        scroll-snap-type: none;
        overflow: visible;
        height: auto;
    }}
    .slide {{
        height: auto;
        min-height: 100vh;
        page-break-after: always;
        overflow: visible;
    }}
    .progress-bar,
    .slide-counter,
    .notes-drawer {{
        display: none !important;
    }}
    .animate-fade-in,
    .animate-slide-up {{
        opacity: 1 !important;
        transform: none !important;
    }}
}}

/* ================================================================
   SCROLLBAR
   ================================================================ */
::-webkit-scrollbar {{
    width: 5px;
}}
::-webkit-scrollbar-track {{
    background: transparent;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(0,200,255,0.2);
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(0,200,255,0.4);
}}

/* ================================================================
   RESPONSIVE — Graceful degradation
   ================================================================ */
@media (max-width: 1024px) {{
    .exec-summary-grid,
    .exhibit-grid,
    .dual-grid,
    .insight-grid,
    .context-grid,
    .two-col-grid,
    .ci-grid,
    .comparison-grid,
    .ba-grid {{
        grid-template-columns: 1fr;
    }}
    .tg-cards-grid {{
        grid-template-columns: repeat(2, 1fr) !important;
    }}
    .comp-vs, .ba-divider {{
        display: none;
    }}
    .hero-text {{
        font-size: 2.5rem;
    }}
    .big-num {{
        font-size: 5rem;
    }}
    .title-main {{
        font-size: 2.2rem;
    }}
    .finding-statement {{
        font-size: 1.6rem;
    }}
}}
"""


# ---------------------------------------------------------------------------
# JavaScript — Full interactivity
# ---------------------------------------------------------------------------

def _build_js() -> str:
    """Build the complete JS block for keyboard nav, animations, notes."""
    return """
(function() {
    'use strict';

    var slides = document.querySelectorAll('.slide');
    var totalSlides = slides.length;
    var progressBar = document.querySelector('.progress-bar');
    var slideCounter = document.querySelector('.slide-counter');
    var notesDrawer = document.querySelector('.notes-drawer');
    var notesContent = document.querySelector('.notes-content');
    var notesOpen = false;

    // --- Helpers ---

    function getCurrentSlideIndex() {
        var scrollTop = window.scrollY || document.documentElement.scrollTop;
        var winH = window.innerHeight;
        return Math.round(scrollTop / winH);
    }

    function scrollToSlide(index) {
        if (index < 0) index = 0;
        if (index >= totalSlides) index = totalSlides - 1;
        slides[index].scrollIntoView({ behavior: 'smooth' });
    }

    function updateProgress() {
        var idx = getCurrentSlideIndex();
        var pct = totalSlides > 1 ? ((idx) / (totalSlides - 1)) * 100 : 100;
        if (progressBar) progressBar.style.width = pct + '%';
        if (slideCounter) slideCounter.textContent = (idx + 1) + ' / ' + totalSlides;
        updateNotes(idx);
    }

    function updateNotes(idx) {
        if (!notesContent) return;
        var slide = slides[idx];
        if (!slide) return;
        var noteEl = slide.querySelector('.speaker-notes');
        if (noteEl) {
            notesContent.textContent = noteEl.textContent;
        } else {
            notesContent.textContent = '(No speaker notes for this slide)';
        }
    }

    // --- Keyboard navigation ---

    document.addEventListener('keydown', function(e) {
        // Skip if typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        var current = getCurrentSlideIndex();
        var nav = {
            'ArrowDown': 1, 'ArrowRight': 1, ' ': 1, 'PageDown': 1,
            'ArrowUp': -1, 'ArrowLeft': -1, 'PageUp': -1
        };
        if (nav[e.key] !== undefined) {
            scrollToSlide(current + nav[e.key]);
            e.preventDefault();
            return;
        }
        if (e.key === 'Home') { scrollToSlide(0); e.preventDefault(); }
        if (e.key === 'End') { scrollToSlide(totalSlides - 1); e.preventDefault(); }
        if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); e.preventDefault(); }
        if (e.key === 'n' || e.key === 'N') { toggleNotes(); e.preventDefault(); }
    });

    // --- Fullscreen ---

    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(function(){});
        } else {
            document.exitFullscreen().catch(function(){});
        }
    }

    // --- Notes drawer ---

    function toggleNotes() {
        notesOpen = !notesOpen;
        if (notesDrawer) {
            notesDrawer.classList.toggle('open', notesOpen);
        }
        if (notesOpen) {
            updateNotes(getCurrentSlideIndex());
        }
    }

    // --- Scroll-based updates ---

    var scrollTimer = null;
    window.addEventListener('scroll', function() {
        if (scrollTimer) clearTimeout(scrollTimer);
        scrollTimer = setTimeout(updateProgress, 50);
    }, { passive: true });

    // --- IntersectionObserver: staggered reveal ---

    if ('IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

        document.querySelectorAll('.animate-fade-in, .animate-slide-up').forEach(function(el) {
            revealObserver.observe(el);
        });

        // --- IntersectionObserver: counter animation ---

        var counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                if (el.dataset.counted) return;
                el.dataset.counted = '1';

                var text = el.textContent.trim();
                var match = text.match(/^([\\d,.]+)(%|\\+|x|[A-Za-z ]*)?$/);
                if (!match) return;

                var raw = match[1].replace(/,/g, '');
                var target = parseFloat(raw);
                var suffix = match[2] || '';
                var hasDecimal = raw.indexOf('.') !== -1;
                var decimals = hasDecimal ? raw.split('.')[1].length : 0;
                var useComma = match[1].indexOf(',') !== -1;

                if (isNaN(target) || target === 0) return;

                var duration = 1200;
                var start = performance.now();

                function animate(now) {
                    var elapsed = now - start;
                    var progress = Math.min(elapsed / duration, 1);
                    // Ease out cubic
                    var eased = 1 - Math.pow(1 - progress, 3);
                    var current = target * eased;

                    var display;
                    if (hasDecimal) {
                        display = current.toFixed(decimals);
                    } else {
                        display = Math.round(current).toString();
                    }
                    if (useComma) {
                        display = display.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
                    }
                    el.textContent = display + suffix;

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }
                }
                requestAnimationFrame(animate);
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('[data-counter]').forEach(function(el) {
            counterObserver.observe(el);
        });
    }

    // --- Touch support for mobile ---

    var touchStartY = 0;
    var touchStartX = 0;
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.touches[0].clientY;
        touchStartX = e.touches[0].clientX;
    }, { passive: true });

    document.addEventListener('touchend', function(e) {
        var deltaY = touchStartY - e.changedTouches[0].clientY;
        var deltaX = touchStartX - e.changedTouches[0].clientX;
        var current = getCurrentSlideIndex();
        // Only navigate on clear vertical swipe (>60px, mostly vertical)
        if (Math.abs(deltaY) > 60 && Math.abs(deltaY) > Math.abs(deltaX) * 1.5) {
            scrollToSlide(current + (deltaY > 0 ? 1 : -1));
        }
    }, { passive: true });

    // --- Init ---
    updateProgress();
})();
"""


# ---------------------------------------------------------------------------
# Slide assembly
# ---------------------------------------------------------------------------

def _render_slide(slide: SlideModel, mode: str, icon_mgr: IconManager,
                  index: int, total: int, footer_left: str) -> str:
    """Render a single slide to HTML."""
    theme_cls = f"slide-{slide.theme}"
    mode_cls = f"mode-{mode}"

    renderer = _LAYOUT_DISPATCH.get(slide.layout, _render_briefing)
    content_html = renderer(slide, mode, icon_mgr)

    header = _render_slide_header(slide, total)
    footer = _render_slide_footer(slide, footer_left, index, total)
    notes = _render_speaker_notes(slide)

    return (
        f'<div class="slide {mode_cls} {theme_cls}" '
        f'id="slide-{slide.slide_id}" data-index="{index}">'
        f'{header}'
        f'{content_html}'
        f'{footer}'
        f'{notes}'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------

def render_html(presentation: PresentationModel, output_path: str) -> None:
    """Render a PresentationModel to an interactive HTML file.

    Generates a self-contained HTML document with embedded CSS, JS, and
    Chart.js support.  Each slide is a full-viewport section with
    scroll-snap, glassmorphism headers, rich visual components, and
    keyboard navigation.

    Args:
        presentation: The parsed presentation model.
        output_path: Filesystem path for the output HTML file.
    """
    mode = presentation.mode
    icon_mgr = IconManager()

    # Build CSS
    css = _build_css(mode)

    # Render slides
    total = len(presentation.slides)
    slides_html_parts: list[str] = []
    for i, slide in enumerate(presentation.slides):
        slides_html_parts.append(
            _render_slide(slide, mode, icon_mgr, i, total,
                          presentation.footer_left)
        )
    slides_html = "\n".join(slides_html_parts)

    # Build JS
    js = _build_js()

    # Title
    doc_title = _ESC(presentation.title) or "Strategy"

    # Assemble document
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{doc_title}</title>
<meta name="description" content="Content-as-Code Strategy">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{GOOGLE_FONTS_URL}" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
{css}
</style>
</head>
<body>

<div class="progress-bar" style="width:0%;"></div>
<div class="slide-counter">1 / {total}</div>

{slides_html}

<div class="notes-drawer">
<h4>Speaker Notes</h4>
<div class="notes-content">(No speaker notes for this slide)</div>
</div>

<script>
{js}
</script>
</body>
</html>"""

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(document)
