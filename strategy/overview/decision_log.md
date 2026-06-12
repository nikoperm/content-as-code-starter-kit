---
title: "Decision Log"
purpose: "Records strategic decisions with context, rationale, and impact tracking"
status: draft
version: "1.0"
created: 2026-06-12
updated: 2026-06-12
author: agent
domain: overview
related:
  - strategy/overview/execution_framework.md
---

# Decision Log

> Record strategic decisions here using the `decision-log` skill.
> Format: `DEC-YYYY-NNN`

---

### DEC-2026-001: Adopt Content-as-Code for Strategy Management

- **Date**: 2026-06-12
- **Context**: Strategy documents were scattered across SharePoint, email, and PowerPoint. No single source of truth existed, and updates were lost between versions.
- **Decision**: Adopt a Content-as-Code approach — all strategic documents as markdown in git, maintained by AI agents, validated automatically.
- **Alternatives considered**:
  - Confluence wiki — rejected because no version control discipline, pages become stale
  - SharePoint — rejected because no automation, no agent integration
- **Impact**: All strategy work now happens in this workspace. Agents handle formatting, validation, and cross-referencing.
- **Owner**: Strategy team
- **Review date**: 2026-12-01

---

### DEC-2026-002: Structure All Initiatives as Business Opportunities

- **Date**: 2026-06-12
- **Context**: Different teams used different formats for tracking initiatives — some used OKRs, some used project plans, some used nothing.
- **Decision**: Standardize on the Business Opportunity (BO) framework with six required fields: Customer Outcome, Value Proposition, Financial Target, Milestones, Leading Indicators, Owner.
- **Alternatives considered**:
  - OKRs — rejected because they lack financial rigor and customer outcome focus
  - Traditional project plans — rejected because they focus on activities, not outcomes
- **Impact**: All roadmap documents now use BO structure. See [Execution Framework](execution_framework.md).
- **Owner**: Strategy team
- **Review date**: —
