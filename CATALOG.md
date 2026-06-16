---
title: "Document Catalog"
purpose: "Living registry of every document in the Content-as-Code workspace"
status: active
version: "1.0"
created: 2026-06-12
updated: 2026-06-12
author: agent
domain: overview
related: []
---

# Document Catalog

> **For AI Agents**: Read this file FIRST. It is your complete map of the knowledge base.
>
> **This file is auto-generated** by `scripts/generate_catalog.py`. Do not edit manually.
> Run `make catalog` to regenerate.

---

## Strategy & Vision (`strategy/overview/`)

| Document | Path | Status | Purpose |
|:---------|:-----|:-------|:--------|
| Decision Log | [decision_log.md](strategy/overview/decision_log.md) | draft | Records strategic decisions with context, rationale, and impact tracking |
| Execution Framework | [execution_framework.md](strategy/overview/execution_framework.md) | draft | Defines how strategic initiatives are structured, governed, and measured |
| Executive Summary | [executive_summary.md](strategy/overview/executive_summary.md) | draft | High-level overview of the strategic direction and key priorities |

---

## Current State (`strategy/current_state/`)

| Document | Path | Status | Purpose |
|:---------|:-----|:-------|:--------|
| Market Position | [market_position.md](strategy/current_state/market_position.md) | draft | Overview of current market position, competitive landscape, and key metrics |
| Service Catalog | [service_catalog.md](strategy/current_state/service_catalog.md) | draft | Central registry of all customer-facing products and platforms — the definitive source for what each product is and is not |
| Strategic Foundation | [strategic_foundation.md](strategy/current_state/strategic_foundation.md) | draft | Defines mission, vision, strategic pillars, and success factors |
| Team Architecture | [team_architecture.md](strategy/current_state/team_architecture.md) | draft | Overview of team structure, strategic areas, and how teams are organized around value streams |
| Value Stream Snapshot | [value_stream_snapshot.md](strategy/current_state/value_stream_snapshot.md) | draft | Overview of all active Business Opportunities across strategic areas |

---

## Transformation (`strategy/transformation/`)

| Document | Path | Status | Purpose |
|:---------|:-----|:-------|:--------|
| Headcount Transformation | [headcount_transformation.md](strategy/transformation/headcount_transformation.md) | draft | Plans the shift from legacy operations to growth-oriented team allocation |
| Operating Model | [operating_model.md](strategy/transformation/operating_model.md) | draft | Describes the target operating model with AI-first agentic teams |

---

## Roadmap (`strategy/roadmap/`)

| Document | Path | Status | Purpose |
|:---------|:-----|:-------|:--------|
| Customer Solutions Strategy | [customer_solutions_strategy.md](strategy/roadmap/customer_solutions/customer_solutions_strategy.md) | draft | Roadmap for developing tailored B2B solutions for key industry verticals |
| Roadmap Overview | [overview.md](strategy/roadmap/overview.md) | draft | Holistic view of all strategic service areas and their roadmaps |
| Security Strategy — Secure by Design | [security_strategy.md](strategy/roadmap/security/security_strategy.md) | draft | Detailed roadmap for the Secure by Design service area |

---

## Presentation (`strategy/presentation/`)

| Document | Path | Status | Purpose |
|:---------|:-----|:-------|:--------|
| Demo Deck | [demo_deck.md](strategy/presentation/demo_deck.md) | draft | Demonstrates the presentation engine with sample slides and layouts |

---

## Agent Skills (`.agent/skills/`)

| Skill | Path | Purpose |
|:------|:-----|:--------|
| Changelog Generator | [.agent/skills/changelog-generator/SKILL.md](.agent/skills/changelog-generator/SKILL.md) | Generates a human-readable changelog from git history, grouped by strategic domain and change type |
| Decision Log | [.agent/skills/decision-log/SKILL.md](.agent/skills/decision-log/SKILL.md) | Tracks strategic decisions with context, rationale, alternatives considered, and impact |
| Document Lifecycle | [.agent/skills/document-lifecycle/SKILL.md](.agent/skills/document-lifecycle/SKILL.md) | Governs how AI agents create, modify, archive, and maintain documents in the Content-as-Code workspace |
| BO Builder | [.agent/skills/bo-builder/SKILL.md](.agent/skills/bo-builder/SKILL.md) | Creates, validates, and places Business Opportunities with all 6 required fields |
| Presentation Design | [.agent/skills/presentation-design/SKILL.md](.agent/skills/presentation-design/SKILL.md) | Creates premium interactive HTML presentations by writing custom slide HTML directly |
| Quality Gate | [.agent/skills/quality-gate/SKILL.md](.agent/skills/quality-gate/SKILL.md) | Enforces the draft-to-active promotion process |
| Source Extractor | [.agent/skills/source-extractor/SKILL.md](.agent/skills/source-extractor/SKILL.md) | Extracts structured insights from PDF source documents in reference/pdf/ and produces machine-readable markdown files in strategy/insights/ |
| Strategy Review | [.agent/skills/strategy-review/SKILL.md](.agent/skills/strategy-review/SKILL.md) | Perform structured strategy reviews and improvements on business strategy documents |
| Ux Review | [.agent/skills/ux-review/SKILL.md](.agent/skills/ux-review/SKILL.md) | Reviews presentation materials (PDF, PPTX, HTML, A4 documents) for executive-quality design, narrative structure, and Telegrafen compliance |
| Workspace Health | [.agent/skills/workspace-health/SKILL.md](.agent/skills/workspace-health/SKILL.md) | Validates workspace integrity: front-matter compliance, CATALOG |

---

