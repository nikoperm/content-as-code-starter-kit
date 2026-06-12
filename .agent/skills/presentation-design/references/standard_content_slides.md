# Standard Content Slides

Standard strategic content that MUST be consistent across all presentations.
These are not layout patterns (see `layout_catalog.md` for that).
These are canonical strategic content elements — the official organizational
position that agents must reproduce faithfully in every presentation that
includes them.

## How to Use

1. Check which standard content slides are relevant to your presentation type
2. Read the **canonical source** document for current content (it may have been updated)
3. Read the **reference HTML** for the visual implementation
4. Reproduce the content faithfully — do not paraphrase or reinterpret
5. Visual treatment may be adapted to the presentation type, but content must match

**Reference HTML:** `reference_allmote.html` (frozen copy in this skill directory)

---

## 1. Mission Statement

| Field | Value |
|:------|:------|
| **Content** | "Empowering Norwegian businesses with trusted mobile connectivity and digital security — delivering effortless value and exceptional experiences every day" |
| **Canonical source** | `strategy/current_state/strategic_foundation.md` (Section 2) |
| **Reference HTML** | `reference_allmote.html` — popup overlay on Slide 5 (`id="popup-mission"`) |
| **Visual treatment** | Full-screen popup with dark backdrop blur. Centered display text (bold italic, ~3.5rem). Key phrases highlighted with dark-blue `.mp-hl` boxes. Accent words (trusted mobile connectivity, digital security, effortless value, exceptional experiences) in `--tg-telenor-blue` cyan. |
| **When to include** | Every strategy presentation. Required in allmøte and narrative formats. |

---

## 2. Five Strategic Pillars

| Field | Value |
|:------|:------|
| **Content** | 1) Grow revenue market share across Mass Market and Enterprise, 2) Position as the preferred strategic partner for Mission Critical customers, 3) Succeed through a new license model: Easy to understand, buy, and use — simple to build and deliver, 4) Differentiate and grow value through Security, Customer Solutions, and Efficient Administration, 5) Simplify, speed up and enable our business with data and high-impact teams |
| **Canonical source** | `strategy/current_state/strategic_foundation.md` (Section 3) |
| **Reference HTML** | `reference_allmote.html` — popup overlay on Slide 5 (`id="popup-pillars"`) |
| **Icons** | `reference/icons/grow.svg`, `reference/icons/shield.svg`, `reference/icons/2030.svg`, `reference/icons/services.svg`, `reference/icons/simplify.svg` |
| **Visual treatment** | Full-screen popup with dark backdrop. Header: "2026" + "Fem strategiske pilarer". 5-card grid, each card has: icon (122px), description with bold/italic key phrases, KPI metric below divider line. Cards are dark-blue with subtle border, hover lift effect. |
| **KPIs per pillar** | 1) Revenue growth in Mass Market and Large + Growth in ARPU in XL and Public, 2) # of new Mission Critical contracts, 3) Value from 20:30 target picture, 4) Growth in revenue from services, 5) # of active Looker users + increase in team enablement |
| **When to include** | Every strategy presentation. Can be full slide or popup. |

---

## 3. Strategy-to-Execution Chain

| Field | Value |
|:------|:------|
| **Content** | 7-level hierarchy: Selskapsstrategi → Vår misjon → 5 Pilarer → **BO** (hero) → Milepæler/indikatorer → Personlige mål → Team Puls |
| **Canonical source** | `strategy/overview/execution_framework.md` (Section 1) |
| **Reference HTML** | `reference_allmote.html` — Slide 5 (7-column full-bleed layout with `.slide-chain` class) |
| **Visual treatment** | Full-bleed 7-column layout with **click-to-advance sub-stepping** (9 steps total). Columns start hidden (`opacity: 0`) and reveal one by one from left to right via `.col-visible` class. Dynamic arrow (`clip-path` chevron) at top grows proportionally as columns appear, width controlled by `--arrow-width` CSS custom property. Step 2 triggers mission statement popup overlay. Step 4 triggers strategic pillars popup overlay. Popups use dark `rgba(3,2,40,0.92)` backdrop with `blur(12px)`. Columns progress from darkest blue (`#030228`) through green BO hero column (`--tg-accent-green`) to lighter blues. BO column has box-shadow glow. |
| **Selskapsstrategi items** | Skape sammen, Vinne kunden, Ledende på teknologi, Bærekraft i alt vi gjør |
| **When to include** | Governance/operating model presentations, allmøte. The chain is the central visual metaphor for how strategy connects to individual execution. |

---

## 4. Ceremony Flywheel

| Field | Value |
|:------|:------|
| **Content** | 5 governance ceremonies: 1) BO Kick-off (quarterly), 2) BO Review (monthly), 3) State of Mobile (monthly allmøte), 4) Personlige Mål (bi-weekly 1:1), 5) Live Puls (monthly) |
| **Canonical source** | `strategy/overview/execution_framework.md` (Section 4+) |
| **Reference HTML** | `reference_allmote.html` — Slide 8 (interactive flywheel with `.slide-rhythm` class) |
| **Visual treatment** | Dark `.am-ambient` animated gradient background. Grid layout: left 1.15fr (flywheel), right 1fr (detail card). Flywheel: 5 circular nodes (170px) on a dashed circle (80% of 580px wrap), center hub shows current step number. Active node scales to 1.1 and fills with `--tg-telenor-blue`. Arrow keys/clicks step through ceremonies sequentially, intercepting navigation until all 5 visited. Detail card (dark blue, 20px radius, 480px height) cross-fades between ceremony details using `fadeInDetail` animation. Each detail: colored tag pill (green), italic title (2-2.8rem), frequency in cyan, description paragraph, arrow-prefixed bullets. Step indicator at bottom shows "01 / 05" style. Entering from previous slide resets to ceremony 1; entering from next resets to ceremony 5. |
| **Ceremony details** | Each ceremony: tag category (Planlegging/Styring/Kultur & Alignment/Oppfølging/Tidlig signal), title, frequency, description paragraph, 2-3 action bullets with → prefix |
| **When to include** | Governance presentations, operating model introductions, allmøte explaining how we work. |

---

## 5. Collaboration Triangle

| Field | Value |
|:------|:------|
| **Content** | Three actors around central BO: **Teamene** (Effekt & Leveranse), **Verdistrømsledelse** (Retning & Fart), **P&C** (Mennesker & Kultur). Three edges: Strategisk Dialog, Enablement & Læring, Målstyring & Kapasitet. |
| **Canonical source** | `strategy/overview/execution_framework.md` (Section 4) |
| **Reference HTML** | `reference_allmote.html` — Slide 10 (`.slide-collab` class) |
| **Visual treatment** | Dark `.am-ambient` background. Canvas container (max 1200px, 620px height) with SVG connecting paths and absolute-positioned cards. Central BO node: 180px circle with `pulseGlow` animation (radial gradient glow, 3s alternate infinite), inner circle has cyan border, blurred inset shadow, backdrop blur. 3 cards at triangle vertices: **Teamene** (solid `--tg-accent-green` background, dark text, top center), **Verdistrømsledelse** (dark blue card with cyan border accent, bottom-left), **P&C** (dark blue card with pink border accent, bottom-right). SVG dashed lines with `stroke-dasharray="10 6"` and `collabFlow` animation (1.2s linear infinite). Bottom dashed line as HTML element with repeating-linear-gradient and reverse dash animation. 3 edge callout pills (30px border-radius, glass effect) on each triangle edge describing interactions. All cards have hover lift (-5px). Staggered entry animations d1-d5. |
| **When to include** | Governance presentations, role/responsibility discussions, any presentation explaining how teams, leadership, and P&C interact around BOs. |

---

## 6. Three Commitments (Non-Negotiable BO Requirements)

| Field | Value |
|:------|:------|
| **Content** | 1) **Kundegevinst** — Definer hva kunden opplever annerledes. Dette er utgangspunktet. 2) **Tallfestet** — Sett lista så høyt du kan gå oppreist under. 3-årig GP-mål tallfestet — ingen unntak. 3) **Ledende indikatorer** — Mål adferdsendringer kontinuerlig. Sanntidssignaler gir kurskorreksjon før det er for sent. |
| **Canonical source** | `strategy/overview/execution_framework.md` (Section 3.2) |
| **Reference HTML** | `reference_allmote.html` — Slide 11 (`.s10-triptych` class) |
| **Visual treatment** | Full-bleed triptych (3 equal vertical panels, `padding: 0`, `flex-direction: row`). Each panel: white SVG icon (clamp 72-100px), large italic name (clamp 2.5-4rem, weight 900, letter-spacing -3px), white accent divider (64×4px, 2px radius), description text (1rem, weight 500, max 28ch, 85% white opacity). Panel separators: `::before` pseudo-element 1px white at 10% opacity. Colors progress: `#070452` → `var(--tg-mid-blue)` → `#2954FF`. Title bar at bottom with dark-blue highlight box (`box-decoration-break: clone`). Staggered entry with `.anim` d1-d3. |
| **Icons** | `reference/icons/CustomerService_expanded_white.svg` (Kundegevinst), `reference/icons/Deal_expanded_white.svg` (Tallfestet), `reference/icons/Coverage_expanded_white.svg` (Ledende indikatorer) |
| **When to include** | Any presentation introducing or reinforcing the BO framework. These are the three non-negotiables every BO must satisfy. |

---

## 7. BO Showcase (Kick-off Card)

| Field | Value |
|:------|:------|
| **Content** | Example BO presented in kick-off card format showing: BO name, pillar tag, customer outcome, value for Telenor, GP targets (yearly + total), key milestones, and leading indicators. |
| **Canonical source** | Content varies per presentation — use a real BO from `strategy/roadmap/` |
| **Reference HTML** | `reference_allmote.html` — Slide 6 (`.slide-bo-showcase` class) |
| **Visual treatment** | Dark `.am-ambient` background. Grid `1fr 1fr` layout. **Left card** (`.bo-kick-top`): solid `--tg-dark-blue` with left-rounded corners (20px). Green pill tag with pillar name. BO name as h3 (2rem, 900 weight). Customer Outcome and Value for Telenor sections with italic titles and cyan uppercase question sub-labels. GP target bar: flex row of rounded cells showing yearly values and total (total cell has cyan border highlight). **Right card** (`.bo-kick-bottom`): semi-transparent glass (`rgba(255,255,255,0.06)`, `backdrop-filter: blur(8px)`), right-rounded corners. Hidden initially (`opacity: 0 !important`), revealed via click with `.card-visible` class. Shows detailed customer outcomes, milestones (bold quarter prefixes), and leading indicators as bullet lists with cyan bullet markers. Footer title bar at absolute bottom. |
| **When to include** | Any governance or operating model presentation. The specific BO featured should be selected for the audience — use the template structure, not the specific example BO. |

---

## 8. Hybrid Teams (Before/After Transformation)

| Field | Value |
|:------|:------|
| **Content** | Before/after comparison: "Dagens Modell" (scattered docs, AI as chatbot) → "Morgendagens AI-first Modell" (integrated human + AI agent collaboration). Three radical shifts: 1) Organisering (4-5 persons + AI agents), 2) Arbeidsmåte (AI-first + GitOps), 3) Roller & Kompetanse (50%+ new roles). |
| **Canonical source** | `strategy/transformation/operating_model.md` |
| **Reference HTML** | `reference_allmote.html` — Slide 9b (`.slide-hybrid-teams` class) |
| **Visual treatment** | Dark `.am-ambient` background. Top: grid `1fr auto 1fr` hero comparison. Old side: transparent background, white text, icon at 96px. New side: white/gradient background (`linear-gradient(135deg, white, #f3fcff)`), 32px border-radius, deep layered box-shadow with ambient cyan glow, dark text. Floating cyan arrow circle between (56px, `htArrowFloat` animation bouncing 8px horizontally). Below: 3-column changes grid separated by thin horizontal line. Each card: large italic cyan number (`01`/`02`/`03`), bold title (hover turns cyan), description. Title bar at absolute bottom with cyan-highlighted "AI-agenter" span. |
| **When to include** | Transformation-focused presentations, operating model introductions. Content adapts based on current transformation status. |

---

## Content That is NOT Standard

These slides use layout patterns from `layout_catalog.md` but contain presentation-specific content. Do **not** reproduce them verbatim — adapt for each audience.

- **Title slide** — event-specific badge, title, date
- **Big Numbers / opening stats** — vary by audience and current data (use counter animations)
- **Problem triptych** — specific to the narrative being told
- **Photo dividers** — selected per narrative arc (use ken-burns zoom effect)
- **Capacity chart / FTE allocation** — data changes frequently (use Chart.js with staggered animation)
- **Closing statement** — audience-specific call to action (use closing-charge layout)
