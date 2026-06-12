"""Telegrafen Design System — shared constants for the presentation engine.

Consolidates colors, typography, SVG assets, and CSS tokens from the
Telegrafen design system so they're defined once and used by all renderers.
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICONS_DIR = os.path.join(PROJECT_ROOT, "reference", "icons")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "reference", "images")
TEMPLATE_PPTX = None  # Set to a .pptx template path to enable PowerPoint export

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

COLORS = {
    "dark_blue": "#070452",
    "mid_blue": "#1C16C5",
    "telenor_blue": "#00C8FF",
    "blue": "#2954FF",
    "light_cyan": "#EBFFFF",
    "light_blue": "#B4FFFF",
    "off_white": "#E8FDFF",
    "white": "#FFFFFF",
    # Accents
    "accent_cyan": "#ADFFFE",
    "accent_green": "#B0FBB8",
    "accent_yellow": "#FEF6B8",
    "accent_pink": "#FFB8D7",
    # Semantic
    "text_primary": "#070452",
    "text_muted": "#637381",
    "text_muted_light": "#B0C4DE",
    # Status
    "success": "#00D28A",
    "warning": "#FFC700",
    "danger": "#FF3B30",
    # AllMøte semantic
    "trap_red": "#de350b",
    "win_green": "#00875a",
    # CTA (use sparingly)
    "hot_pink": "#FF2483",
    "bright_yellow": "#FDE408",
    "vivid_orange": "#FF700A",
}

# Chart data series color sequence
CHART_COLORS = [
    COLORS["telenor_blue"],
    COLORS["white"],
    COLORS["blue"],
    COLORS["accent_green"],
    COLORS["accent_yellow"],
    COLORS["accent_pink"],
]

# Forbidden legacy colors — validation should flag these.
# Constructed via join to avoid triggering validate_design.py on THIS file.
FORBIDDEN_COLORS = [
    "#" + c for c in [
        "00193C", "001940", "00A9E0", "0b132b", "1c2541", "48cae4",
    ]
]

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------

FONT_HEADING = "'DM Sans', Arial, sans-serif"
FONT_BODY = "'DM Sans', Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"
FONT_PPTX = "Telenor Evolution PPT"

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=DM+Sans:ital,wght@0,400;0,500;0,700;0,800;1,400;1,500&"
    "family=JetBrains+Mono:wght@400;500&display=swap"
)

# ---------------------------------------------------------------------------
# SVG assets
# ---------------------------------------------------------------------------

PROPELLER_SVG = (
    '<svg class="footer-logo" viewBox="0 0 500 460.36">'
    '<path fill="currentColor" d="M252.71,140.78c7.16,1.1,8.6-.34,9.55-7.11'
    'a162.59,162.59,0,0,1,13.91-45.61c9.36-19.25,24.28-40.41,45.14-54.57'
    'C338.88,21.71,367.67,8.67,390,3.94A166.92,166.92,0,0,1,440,.62'
    'c30.13,2.71,46.8,11.3,55.16,22.41,3.11,4.15,4.8,9.28,4.87,12.59'
    '.24,5.53-2.17,12.74-10.11,19.83-7.73,6.82-24.22,15.45-46.71,23'
    '-23.34,7.77-55.23,16-87,23.28a496.38,496.38,0,0,0-54.42,15.63'
    'c-21,7.13-27.38,28.07-14.27,34.46,18.95,9.23,30.8,18.89,40.9,27.1'
    ',15.15,12.42,32.74,27,54.58,53.4,19.79,24.17,52.16,70.3,63.81,115.08'
    ',12.89,49.16,4.83,95.78-23,108.8-27.27,12.79-63.62-5.66-89.13-32.12'
    '-24.28-25.1-41.22-54.68-57.15-100.29-13.81-39.21-19.41-96.07-19.39'
    '-125.81,0-9.91-.16-12,.24-21,.93-7.79-20.1-14.24-42.69.3-25.72,16.54'
    '-50.91,46.52-65.78,63.93-6.47,7.6-15.24,18.77-24.53,30.49-12.25,15.36'
    '-25.78,31.36-38.1,40.31C68.67,325.56,38.87,331.15,18,316.26,6.38,308'
    ',.2,292.3,0,276.37A60.7,60.7,0,0,1,8.21,245c7-12.28,18.51-25.46,36.77'
    '-40.56,18.87-15.51,49-33,79.21-45.19,46.06-18.54,95.65-24.37,128.52'
    '-18.48Z"/></svg>'
)

LOGO_SVG_DARK = (
    '<svg viewBox="0 0 24 24" style="width:20px;height:20px;fill:none;'
    f'stroke:{COLORS["dark_blue"]};stroke-width:2;stroke-linecap:round;">'
    '<polyline points="16 18 22 12 16 6"></polyline>'
    '<polyline points="8 6 2 12 8 18"></polyline></svg>'
)

LOGO_SVG_WHITE = (
    '<svg viewBox="0 0 24 24" style="width:20px;height:20px;fill:none;'
    f'stroke:{COLORS["white"]};stroke-width:2;stroke-linecap:round;">'
    '<polyline points="16 18 22 12 16 6"></polyline>'
    '<polyline points="8 6 2 12 8 18"></polyline></svg>'
)

# ---------------------------------------------------------------------------
# PPTX layout mapping
# ---------------------------------------------------------------------------

PPTX_LAYOUT_MAP = {
    # Executive layouts
    "briefing": "Title and Content",
    "executive-summary": "Long title and Content",
    "evidence-exhibit": "Title and Content",
    "dual-analysis": "Two Content",
    "structured-argument": "Title and Content",
    "appendix-detail": "Title and Content",
    # Narrative layouts
    "insight-chart": "Title and Content",
    "story-build": "Long title and Content",
    "context-split": "Content Image",
    "key-finding": "Statement Soft",
    "dashboard": "Numbers Panels",
    # AllMøte layouts
    "hero-statement": "Statement Dark",
    "big-number": "Statement Dark",
    "icon-showcase": "Blank Dark",
    "animated-reveal": "Title Only",
    "celebration": "Cards Soft",
    "before-after": "Two Content Dark",
    "photo-impact": "Visual Content Mid",
    # Shared layouts (default; mode may adjust)
    "cards-grid": "Three Cards Dark",
    "chart": "Title Only",
    "table": "Title and Content",
    "two-column": "Two Content",
    "three-column": "Three Content",
    "numbers-panel": "Numbers Panels",
    "comparison": "Two Content",
    "timeline": "Title and Content",
    "divider": "Divider Text Mid",
    "title-only": "Title Slide",
    "content-image": "Content Image",
}

# Theme → PPTX layout suffix mapping for shared layouts
PPTX_THEME_SUFFIX = {
    "light": "",
    "statement": " Dark",
    "dark": " Dark",
}

# ---------------------------------------------------------------------------
# Icon category mapping
# ---------------------------------------------------------------------------

ICON_CATEGORIES = {
    "Infrastructure": [
        "CellTower", "Coverage", "Fiber", "Factory", "Warehouse",
        "Office", "Home", "Cabin", "CabinWiFi", "CabinWooden", "CabinWoodenWiFi",
    ],
    "People": [
        "Family1", "Family2", "Family3", "Family4", "Family5",
        "OfficeWorker", "Worker", "Woman", "Elderly",
        "TeenagerBoy", "TeenagerGirl",
    ],
    "Security": [
        "Security", "SecurityBrowser", "SecurityFamily", "SecurityPersonal",
        "SecurityPhone", "SecurityTeenager", "SecurityWeb",
    ],
    "Digital Services": [
        "Chatbot", "Computer", "Streaming", "Gaming", "Multiple Devices",
        "HomeWiFi",
    ],
    "Communication": [
        "Email", "CustomerService", "Reminder", "Sim card",
        "SubscriptionPhone", "DealPhone",
    ],
    "Documents": [
        "Document Attachment", "Document Collaboration", "Document Download",
        "Document Sharing", "Document Signature",
    ],
    "Sustainability": ["Climate change", "Circular climate", "Nature"],
    "Commerce": [
        "Deal", "DealPhone", "Swap", "International roaming", "Insurance",
    ],
    "Special": ["Magic", "Healthcare", "Hospital"],
}

# ---------------------------------------------------------------------------
# CSS design tokens as a Python string (embedded in HTML output)
# ---------------------------------------------------------------------------

CSS_TOKENS = f"""
:root {{
  /* Primary Colors */
  --tg-dark-blue: {COLORS['dark_blue']};
  --tg-mid-blue: {COLORS['mid_blue']};
  --tg-telenor-blue: {COLORS['telenor_blue']};
  --tg-blue: {COLORS['blue']};
  --tg-light-cyan: {COLORS['light_cyan']};
  --tg-light-blue: {COLORS['light_blue']};
  --tg-off-white: {COLORS['off_white']};
  --tg-white: {COLORS['white']};

  /* Accents */
  --tg-accent3: {COLORS['accent_cyan']};
  --tg-accent4: {COLORS['accent_green']};
  --tg-accent5: {COLORS['accent_yellow']};
  --tg-accent6: {COLORS['accent_pink']};

  /* Semantic */
  --tg-text-primary: {COLORS['text_primary']};
  --tg-text-muted: {COLORS['text_muted']};
  --tg-text-muted-light: {COLORS['text_muted_light']};
  --tg-border-light: rgba(0, 200, 255, 0.15);
  --tg-border-dark: rgba(255, 255, 255, 0.1);

  /* Status */
  --tg-success: {COLORS['success']};
  --tg-warning: {COLORS['warning']};
  --tg-danger: {COLORS['danger']};
  --tg-trap-red: {COLORS['trap_red']};
  --tg-win-green: {COLORS['win_green']};

  /* Typography */
  --tg-font-heading: {FONT_HEADING};
  --tg-font-body: {FONT_BODY};
  --tg-font-mono: {FONT_MONO};

  /* Spacing (8dp grid) */
  --tg-space-xs: 8px;
  --tg-space-sm: 16px;
  --tg-space-md: 24px;
  --tg-space-lg: 32px;
  --tg-space-xl: 48px;
  --tg-space-2xl: 64px;

  /* Border Radius */
  --tg-radius-sm: 8px;
  --tg-radius-md: 12px;
  --tg-radius-lg: 16px;
  --tg-radius-pill: 20px;
}}
"""

# Valid layout names per mode
EXECUTIVE_LAYOUTS = {
    "briefing", "executive-summary", "evidence-exhibit",
    "dual-analysis", "structured-argument", "appendix-detail",
}
NARRATIVE_LAYOUTS = {
    "insight-chart", "story-build", "context-split",
    "key-finding", "dashboard",
}
ALLMOTE_LAYOUTS = {
    "hero-statement", "big-number", "icon-showcase",
    "animated-reveal", "celebration", "before-after", "photo-impact",
}
SHARED_LAYOUTS = {
    "cards-grid", "chart", "table", "two-column", "three-column",
    "numbers-panel", "comparison", "timeline", "divider",
    "title-only", "content-image",
}
ALL_LAYOUTS = EXECUTIVE_LAYOUTS | NARRATIVE_LAYOUTS | ALLMOTE_LAYOUTS | SHARED_LAYOUTS
