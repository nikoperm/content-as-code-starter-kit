# Chart Specification

Inline chart YAML definition format and macro reference for data visualization.

---

## Supported Chart Types

| Type           | YAML value      | Best for                                       |
|:---------------|:----------------|:-----------------------------------------------|
| Bar            | `bar`           | Comparisons across categories or time periods  |
| Line           | `line`          | Trends over time, trajectory                   |
| Doughnut       | `doughnut`      | Proportions of a whole (max 5-6 segments)      |
| Stacked Bar    | `stacked-bar`   | Composition breakdown across categories        |
| Combo          | `combo`         | Bar + line overlay (e.g., volume + growth rate) |

---

## Inline Chart YAML Structure

```yaml
<!-- chart:
  type: bar                          # Required: chart type
  title: "Gross Profit Scenarios"    # Optional: rendered above the chart
  data:
    labels: [2025, 2026, 2027, 2028, 2029]   # X-axis categories
    series:
      - name: Baseline               # Legend label
        values: [4480, 4551, 4461, 4371, 4281]
        color: "#070452"             # Optional: hex color override
      - name: Target
        values: [4480, 4700, 4900, 5100, 5300]
        color: "#00C8FF"
        type: line                   # Optional: override type for this series (combo charts)
  annotation: "+603 mNOK gap"       # Optional: callout box text
-->
```

### Data Fields

| Field                  | Required | Description                                          |
|:-----------------------|:---------|:-----------------------------------------------------|
| `type`                 | Yes      | Chart type (see table above)                         |
| `title`                | No       | Chart heading rendered above the canvas              |
| `data.labels`          | Yes      | Array of x-axis labels                               |
| `data.series`          | Yes      | Array of data series objects                         |
| `data.series[].name`   | Yes      | Legend label for the series                          |
| `data.series[].values` | Yes      | Array of numeric values (must match labels length)   |
| `data.series[].color`  | No       | Hex color override. Defaults to CHART_COLORS palette |
| `data.series[].type`   | No       | Per-series type override (for combo charts)          |
| `annotation`           | No       | Text for the insight callout box                     |

---

## Annotation Positioning

The annotation callout box is positioned at top-right of the chart container:

- Semi-transparent background with Telenor Blue border
- Bold text at 0.85rem
- Used to highlight the key insight (e.g., "+603 mNOK gap", "2x growth")

Every chart should have an annotation. If you cannot state the "so what?" in 5 words, reconsider the chart's purpose.

---

## Color Recommendations (Telegrafen Palette)

Default series color rotation (applied automatically when no `color` specified):

| Order | Color            | Hex       | Use for                      |
|:------|:-----------------|:----------|:-----------------------------|
| 1     | Telenor Blue     | `#00C8FF` | Primary/highlight series     |
| 2     | White            | `#FFFFFF` | Secondary comparison series  |
| 3     | Blue             | `#2954FF` | Third series                 |
| 4     | Accent Green     | `#B0FBB8` | Positive / growth indicators |
| 5     | Accent Yellow    | `#FEF6B8` | Neutral / caution indicators |
| 6     | Accent Pink      | `#FFB8D7` | Alert / risk indicators      |

**Semantic colors for specific contexts:**
- Success / wins: `#00D28A`
- Warning: `#FFC700`
- Danger / risk: `#FF3B30`
- "Trap" / legacy problems: `#de350b`
- "Win" / achievements: `#00875a`

Never use colors outside the Telegrafen palette. Forbidden legacy colors will trigger validation errors.

---

## Existing Macro List

Reference pre-built chart functions using `[[MACRO_NAME]]` syntax:

| Macro                          | Description                                          |
|:-------------------------------|:-----------------------------------------------------|
| `[[GP_SCENARIOS_CHART]]`       | Gross Profit baseline vs. target gap visualization   |
| `[[NEEDS_CHART]]`             | 4-quadrant customer needs (Pain vs. Need)            |
| `[[GROWTH_OVERVIEW_CHART]]`   | Five growth pillars overview with GP targets          |
| `[[SECURITY_GROWTH_CHARTS]]`  | Security pillar GP growth projections                |
| `[[CUSTOMER_SOLUTIONS_CHARTS]]` | Customer Solutions pillar GP growth projections     |
| `[[ADVANCED_5G_IOT_CHARTS]]`  | Advanced 5G and IoT pillar GP growth projections     |
| `[[EFFICIENT_ADMIN_CHARTS]]`  | Efficient Admin pillar GP growth projections          |
| `[[LEGACY_TRAP_CHART]]`       | FTE distribution donut (Run vs. Keep vs. Grow)       |
| `[[AGENTIC_WOW_VISUAL]]`      | Agentic WoW architecture and workflow visual         |
| `[[HEADCOUNT_CHART]]`         | Headcount transformation 2025 to 2030                |
| `[[ROADMAP_CHART]]`           | 4-phase transformation roadmap                       |
| `[[TIMELINE_CHART]]`          | Unified timeline with business + agentic milestones  |

Macros are expanded during `make build`. If a macro is not found, a placeholder card is rendered with an error message.

---

## Truncated Y-Axis — Axis Break Plugin

When a chart's y-axis does not start at zero (e.g., `min: 4000` for values around 4000–5000), you **must** add a visual axis break to avoid misleading the audience. The standard is two diagonal lines with a background-colored band between them, drawn near the base of each bar.

### Plugin Implementation

```javascript
var axisBreakPlugin = {
    id: 'axisBreak',
    afterDatasetsDraw: function(chart) {
        var ctx = chart.ctx;
        var yScale = chart.scales.yBar || chart.scales.y;
        if (!yScale) return;
        var barMeta = chart.getDatasetMeta(0);
        var yBottom = yScale.getPixelForValue(yScale.min);
        var gap = 7;      // half-height of the break band
        var slant = 8;    // diagonal tilt in px
        var breakY = yBottom - 50;  // distance from bottom of chart area
        for (var i = 0; i < barMeta.data.length; i++) {
            var bar = barMeta.data[i];
            if (!bar) continue;
            // Animate with bars: fade in as bar grows past break point
            var barTop = bar.y;
            if (barTop > breakY - gap) continue;
            var dist = (breakY - gap) - barTop;
            var opacity = Math.min(1, dist / 40);
            var halfW = bar.width / 2;
            var cx = bar.x;
            ctx.save();
            ctx.globalAlpha = opacity;
            // Fill band between lines with slide background color
            ctx.fillStyle = '#1C16C5';  // match slide background (--tg-mid-blue)
            ctx.beginPath();
            ctx.moveTo(cx - halfW, breakY - gap + slant);
            ctx.lineTo(cx + halfW, breakY - gap - slant);
            ctx.lineTo(cx + halfW, breakY + gap - slant);
            ctx.lineTo(cx - halfW, breakY + gap + slant);
            ctx.closePath();
            ctx.fill();
            // Draw diagonal break lines
            ctx.strokeStyle = 'rgba(255,255,255,0.7)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(cx - halfW - 4, breakY - gap + slant);
            ctx.lineTo(cx + halfW + 4, breakY - gap - slant);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(cx - halfW - 4, breakY + gap + slant);
            ctx.lineTo(cx + halfW + 4, breakY + gap - slant);
            ctx.stroke();
            ctx.restore();
        }
    }
};
```

### Usage Rules

| Rule | Detail |
|:-----|:-------|
| When to use | Any bar chart where `y.min > 0` (truncated axis) |
| Fill color | Must match the slide's background color (`#1C16C5` for mid-blue, `#070452` for dark-blue) |
| Animation | Break marks fade in as bars grow past them during chart entry animation |
| Registration | Add to `plugins: [axisBreakPlugin]` in the Chart constructor |
| Scale reference | Use `chart.scales.yBar` for dual-axis charts, `chart.scales.y` for single-axis |
| Adjustable values | `breakY` offset (distance from bottom), `gap` (band thickness), `slant` (diagonal angle) |

### When NOT to Use

- Charts where y-axis starts at zero — no break needed
- Line-only charts — break marks are a bar chart convention
- Doughnut/pie charts — not applicable

---

## Mode-Specific Chart Styling

| Mode      | Chart treatment                                                        |
|:----------|:-----------------------------------------------------------------------|
| Executive | Annotated "exhibit": chart + takeaway box + source footnotes. Static.  |
| Narrative | Chart with insight annotation + key takeaway text. 800ms animation.    |
| AllMote   | Dramatic reveal: chart animates in, single insight annotation appears. |

- **Executive:** Animation disabled (`duration: 0`). Charts must be fully interpretable as static images for PDF/print.
- **Narrative/AllMote:** Animation enabled (`duration: 800ms`). Data series animate in for visual engagement.
