"""Chart Renderer — generates Chart.js visualizations and wraps existing macros.

Supports two modes:
1. Inline chart specs (from <!-- chart: ... --> YAML blocks)
2. Existing macro references ([[GP_SCENARIOS_CHART]], etc.) via build_html.py
"""

import os
import sys
import json

from .telegrafen import COLORS, CHART_COLORS, PROJECT_ROOT
from .slide_parser import ChartSpec

SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def _get_macro_map() -> dict:
    """Import build_html and return the macro-to-function mapping."""
    try:
        import build_html  # noqa: may fail if build_html has syntax errors
        return {
            "GP_SCENARIOS_CHART": build_html.build_gp_scenarios_chart,
            "NEEDS_CHART": build_html.build_needs_chart,
            "GROWTH_OVERVIEW_CHART": build_html.build_growth_overview_chart,
            "SECURITY_GROWTH_CHARTS": build_html.build_security_growth_charts,
            "CUSTOMER_SOLUTIONS_CHARTS": build_html.build_customer_solutions_charts,
            "EFFICIENT_ADMIN_CHARTS": build_html.build_efficient_admin_charts,
            "LEGACY_TRAP_CHART": build_html.build_legacy_trap_chart,
            "AGENTIC_WOW_VISUAL": build_html.build_agentic_wow_visual,
            "HEADCOUNT_CHART": build_html.build_headcount_chart,
            "HEADCOUNT_TRAJECTORY_CHART": build_html.build_headcount_trajectory_chart,
            "ROADMAP_CHART": build_html.build_roadmap_chart,
            "TIMELINE_CHART": build_html.build_timeline_chart,
            "ADVANCED_5G_IOT_CHARTS": build_html.build_advanced_5g_iot_charts,
        }
    except (ImportError, SyntaxError):
        return {}


def render_macro(macro_name: str) -> str:
    """Render an existing macro by name, returning HTML."""
    macro_map = _get_macro_map()
    func = macro_map.get(macro_name)
    if func:
        return func()
    return f'<div class="tg-card" style="padding:32px;text-align:center;color:var(--tg-text-muted);">Chart macro [{macro_name}] not found</div>'


def render_inline_chart(spec: ChartSpec, mode: str = "narrative") -> str:
    """Render an inline ChartSpec as a Chart.js HTML block."""
    canvas_id = spec.chart_id or "inline_chart"
    labels = json.dumps(spec.data.get("labels", []))

    datasets = []
    for i, series in enumerate(spec.data.get("series", [])):
        color = series.get("color", CHART_COLORS[i % len(CHART_COLORS)])
        chart_type = series.get("type", spec.chart_type)
        ds = {
            "label": series.get("name", f"Series {i+1}"),
            "data": series.get("values", []),
            "backgroundColor": color if chart_type == "bar" else "transparent",
            "borderColor": color,
            "borderWidth": 2,
            "tension": 0.3,
        }
        if chart_type == "line" and spec.chart_type != "line":
            ds["type"] = "line"
            ds["order"] = 0
        datasets.append(ds)

    datasets_json = json.dumps(datasets)

    annotation_html = ""
    if spec.annotation:
        annotation_html = f"""
        <div style="position:absolute;top:16px;right:16px;
                    background:rgba(0,200,255,0.15);border:1px solid var(--tg-telenor-blue);
                    border-radius:var(--tg-radius-sm);padding:8px 16px;
                    font-size:0.85rem;font-weight:700;color:var(--tg-telenor-blue);">
            {spec.annotation}
        </div>"""

    show_animation = mode in ("narrative", "allmote")

    return f"""
    <div class="tg-chart-container" style="position:relative;">
        {f'<h3 style="margin:0 0 16px 0;font-size:1.1rem;font-weight:700;color:var(--tg-white);">{spec.title}</h3>' if spec.title else ''}
        {annotation_html}
        <canvas id="{canvas_id}" style="max-height:300px;"></canvas>
        <script>
        (function() {{
            const ctx = document.getElementById('{canvas_id}');
            if (!ctx) return;
            new Chart(ctx, {{
                type: '{spec.chart_type}',
                data: {{
                    labels: {labels},
                    datasets: {datasets_json}
                }},
                options: {{
                    responsive: true,
                    animation: {{ duration: {800 if show_animation else 0} }},
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#FFFFFF', font: {{ family: "'DM Sans'" }} }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            ticks: {{ color: '#B0C4DE', font: {{ family: "'DM Sans'" }} }},
                            grid: {{ color: 'rgba(255,255,255,0.1)' }}
                        }},
                        y: {{
                            ticks: {{ color: '#B0C4DE', font: {{ family: "'DM Sans'" }} }},
                            grid: {{ color: 'rgba(255,255,255,0.1)' }}
                        }}
                    }}
                }}
            }});
        }})();
        </script>
    </div>
    """


def expand_macros_in_html(html: str) -> str:
    """Replace all [[MACRO_NAME]] placeholders in HTML with rendered charts."""
    import re
    macro_map = _get_macro_map()

    for macro_name, func in macro_map.items():
        placeholder = f"[[{macro_name}]]"
        escaped = f"&gt; [[{macro_name}]]"
        if placeholder in html or escaped in html:
            rendered = func()
            html = html.replace(placeholder, rendered)
            html = html.replace(escaped, rendered)
            html = html.replace(
                f"<blockquote>\n{rendered}\n</blockquote>", rendered
            )
            html = html.replace(
                f"<blockquote>{rendered}</blockquote>", rendered
            )

    return html
