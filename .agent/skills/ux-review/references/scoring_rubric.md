# UX Review Scoring Rubric

Detailed criteria for scoring each dimension from 1 to 10.

---

## 1. Visual Design & Layout (25%)

The single most important dimension. This is what the audience sees before they read a single word. **Score this with extreme rigor.** Most generated decks score 4-6 here, not 7+.

| Score | Criteria |
|-------|----------|
| 1-2 | No visual system. Random fonts, sizes, colors. Zero intentional whitespace. Looks like raw markdown rendered into a box. |
| 3 | Some structure but fundamentally broken: font sizes vary randomly across slides, margins are inconsistent, cards have different padding, elements are misaligned. |
| 4 | Basic layout works but typography is flat — title, body, and labels are too close in size (less than 1.5x difference). Line-height too tight (< 1.5). Whitespace is leftover, not designed. |
| 5 | Telegrafen colors used correctly. Consistent header/footer. But the slides feel *generated*, not *designed*: uniform monotony, no visual anchors, content fills space evenly instead of creating emphasis. Orphan words and awkward line breaks present. |
| 6 | Intentional hierarchy exists (title clearly dominant, content subordinate). Margins consistent within slides. But cross-slide consistency breaks: some slides cramped, others sparse. Cards or containers used but without consistent sizing. Font weights used for emphasis but not consistently. |
| 7 | Strong hierarchy and consistent spacing throughout. 8dp grid adhered to. Typography scale has clear levels (display → title → body → caption) with at least 1.5x size difference between levels. Whitespace is intentional. But the deck has no visual *moments* — every slide follows the same formula. |
| 8 | **McKinsey baseline.** Every slide has a clear visual anchor (the ONE thing your eye hits first). Typography scale creates effortless reading order. Color used semantically. Padding, margins, and gaps pixel-consistent across all slides. Card heights matched. No orphan words. Line breaks fall at natural reading points. |
| 9 | **Pitch-winning.** Masterful variety in layout: some slides use cards, others use hero numbers, others use full-bleed data. Visual rhythm across the deck — the eye and brain get variety without chaos. Statement slides create memorable "pause" moments. Every element has earned its pixels. |
| 10 | **Iconic.** Every slide could be framed. The design is inseparable from the content — it doesn't just display the strategy, it embodies it. Perfect balance of density and breathing room. Would be studied as a reference. |

**Score caps (automatic ceiling — cannot score above this regardless of other qualities):**
- Any non-Telegrafen color → max 5
- Font sizes vary randomly across slides (not a deliberate scale) → max 4
- Inconsistent margins or padding (varies by more than 4px across slides) → max 5
- Every slide uses identical layout → max 6
- Line-height below 1.5 on body text → max 5
- Orphan words on more than 3 slides → max 6
- Card or container padding inconsistent within a single slide → max 5
- No visual anchor (everything same visual weight) on any slide → max 4
- Body text below 0.8rem → max 6
- Header/footer format inconsistent across slides → max 5

**The "generated content" trap:** AI-generated slide decks almost always score 4-6 here because they treat every slide identically. If the deck looks like a template was filled in 37 times, it's a 5 — no matter how clean the template is.

---

## 2. Information Architecture (15%)

How the information is organized for human comprehension.

| Score | Criteria |
|-------|----------|
| 1-3 | No logical grouping. Related information scattered across slides. No progression from simple to complex. |
| 4-5 | Sections exist but transitions are abrupt. Some slides try to cover 3+ topics. The reader loses the thread. |
| 6 | Clear sections with appropriate headers. Each slide has a topic. But the ordering feels arbitrary — could be shuffled without impact. |
| 7 | Logical build-up: context → problem → solution → evidence → next steps. Progressive disclosure works. Preread slides correctly separated from main deck. |
| 8 | **Consulting standard.** The deck structure itself tells a story. Each section has a clear purpose. Supporting detail is available but doesn't compete with the main message. |
| 9 | **Effortless comprehension.** Reader never needs to "go back" to understand something. Every slide builds on the previous one. Complex information feels simple. |
| 10 | **The audience anticipates what comes next.** The structure is so natural that it feels inevitable. Perfect pacing: the right information at the right moment. |

**Score caps:**
- More than 5 bullet points per slide → max 6
- No clear section breaks → max 5
- Slides that could be in any order → max 6

---

## 3. Data Visualization (15%)

Numbers and charts that prove the point, not just fill space.

| Score | Criteria |
|-------|----------|
| 1-3 | Raw tables with no visual emphasis. Charts have no labels. The data doesn't support the slide's message. |
| 4-5 | Charts exist but wrong type chosen (pie chart for trends, bar chart for composition). Labels are too small. No callout of the key number. |
| 6 | Correct chart types. Readable labels. But the chart doesn't "pop" — the key insight is buried in the data. The audience must do mental math. |
| 7 | Key numbers are called out (bold, larger font, accent color). Chart titles state the insight, not the topic ("Revenue grew 23%" not "Revenue Chart"). Clear legends. |
| 8 | **The chart makes the argument.** One glance tells the story. Unnecessary data removed. Visual weight draws the eye to the conclusion. Comparison and trend are immediately obvious. |
| 9 | **The number is the hero.** A single, massive KPI visible from 10 meters away. Supporting data is subordinate. The visualization creates an emotional response (pride, urgency). |
| 10 | **Infographic quality.** The data visualization itself is shareable. Perfect balance of precision and impact. Could be understood by someone who doesn't speak the language. |

**Score caps:**
- Charts with no title or insight label → max 5
- More than 6 data series in one chart → max 6
- Key number not visually prominent → max 7
- Tables with 5+ columns → max 6

---

## 4. Narrative Arc (15%)

The golden thread that makes 37 slides feel like one story.

| Score | Criteria |
|-------|----------|
| 1-3 | No story. Slides are a collection of facts. Could be in any order. No "so what?" |
| 4-5 | A topic exists but no tension/resolution. Reads like a report, not a presentation. |
| 6 | Clear beginning (context), middle (content), end (summary). But no emotional arc — the audience doesn't feel the urgency or the opportunity. |
| 7 | Situation → Complication → Resolution structure. The audience understands WHY transformation is needed before seeing HOW. Each section has a clear transition. |
| 8 | **McKinsey Pyramid.** Slide titles alone tell the complete story. Every slide answers "so what?" The audience can't argue with the logic. |
| 9 | **Memorable.** The audience walks away with 3 things they can repeat. The story has heroes and villains (the legacy trap vs. the 20:30 vision). Tension builds and resolves. |
| 10 | **Transforms thinking.** The audience enters with one mental model and leaves with a new one. The presentation creates a before/after moment. Years later, people reference "that deck." |

**Score caps:**
- Slide titles are topic labels ("Revenue Overview") not insights → max 5
- No clear "why" before "how" → max 6
- No single memorable takeaway → max 7

---

## 5. Emotional Impact (10%)

Does the presentation make people feel something?

| Score | Criteria |
|-------|----------|
| 1-3 | Clinical and dry. Could be a spreadsheet. Zero emotional connection. |
| 4-5 | Competent but forgettable. The audience nods but doesn't lean forward. |
| 6 | Some energy in key slides but inconsistent. The opening or closing has punch but the middle sags. |
| 7 | Consistent professional confidence throughout. Strategic use of bold statements and contrast (problem → solution) creates engagement. |
| 8 | **The audience is invested.** They care about the outcome. The problem feels real, the solution feels achievable, and the urgency feels personal. |
| 9 | **Standing ovation energy.** Multiple "aha" moments. The deck creates alignment and enthusiasm. People want to be part of this story. |
| 10 | **Movement-starting.** The presentation doesn't just inform — it recruits believers. People leave the room wanting to tell others about this vision. |

---

## 6. Executive Readiness (10%)

Would the C-suite take action based on this?

| Score | Criteria |
|-------|----------|
| 1-3 | Would embarrass the presenter. Typos, inconsistencies, unfinished sections. |
| 4-5 | Content is there but the presentation doesn't command respect. Feels like middle management, not leadership. |
| 6 | Professional enough but lacks the authority and precision executives expect. Missing: risk assessment, financial rigor, or clear asks. |
| 7 | **Board-ready.** Clear financial targets, risk mitigation, timeline. The audience trusts the analysis. |
| 8 | **Decision-ready.** The deck has a clear "ask" and gives the board everything they need to say yes or no. No follow-up questions needed. |
| 9 | **CEO would present this.** The deck is so clear and compelling that the CEO would use it in their own investor meeting with minimal changes. |
| 10 | **Boardroom gold.** Combines strategic vision with operational precision. Every skeptic question is pre-answered. The deck itself is evidence of execution capability. |

---

## 7. Brand & Telegrafen Compliance (5%)

Strict adherence to telegrafen.telenor.no design system.

| Score | Criteria |
|-------|----------|
| 1-5 | Uses non-Telegrafen colors or fonts. Missing footer, propeller, or "Sensitivity" label. |
| 6-7 | Correct colors and fonts but inconsistent application. Some elements off-grid. Spacing not 8dp-aligned. |
| 8 | Full compliance. All colors from Telegrafen palette. DM Sans / Telenor Evolution. Footer complete. 8dp grid. |
| 9 | Compliance + tasteful use of secondary palette. Color conveys meaning (not just decoration). |
| 10 | **The Telegrafen team would showcase this as a reference implementation.** Every component feels native to the design system. |

**Automatic scores:**
- Any forbidden color (#00193C, #00A9E0, #0b132b) → max 3
- Wrong font (Outfit, Inter, Calibri) → max 4
- Missing Telenor propeller in footer → max 6

---

## 8. Technical Quality (5%)

Does it render correctly everywhere?

| Score | Criteria |
|-------|----------|
| 1-3 | Broken rendering. Missing characters. Layout shifts. CSS artifacts visible. |
| 4-5 | Renders but with visible issues: wrong line breaks, overlapping text, inconsistent spacing. |
| 6-7 | Clean rendering but minor issues: slightly compressed text, suboptimal font kerning. |
| 8 | **Clean rendering everywhere.** macOS Preview, Chrome, PowerPoint — all look identical. Norwegian characters (æøå) render correctly. |
| 9 | Perfect rendering + responsive behavior. |
| 10 | **Pixel perfect.** No rendering differences across any platform. PDF file is optimized. Fast loading. |

**Automatic scores:**
- `background-clip: text` in PDF → max 4
- Missing æøå → max 5
- CSS `drop-shadow` artifacts → max 5
