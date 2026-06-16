---
title: "Service & Product Catalog"
purpose: "Central registry of all customer-facing products and platforms — the definitive source for what each product is and is not"
status: draft
version: "1.0"
created: 2026-06-15
updated: 2026-06-15
author: agent
domain: current_state
related:
  - strategy/current_state/value_stream_snapshot.md
  - strategy/current_state/market_position.md
---

# Service & Product Catalog

> **Agents: read this before creating BOs, presentations, or proposals involving any product.**
> Misrepresenting a product is worse than not mentioning it. If a product is not listed here, ask the user before assuming what it does.

> **This is a template.** Replace the example products below with your organization's real products. The format and structure are what matter -- the examples are fictional.

---

## Security Services

### SecureShield

Cloud-based endpoint protection platform that guards employees against phishing, malicious links, and social engineering attacks. Evolving into a holistic human risk management service.

- **What it is**: Link protection, security awareness training, proactive threat detection for mobile users
- **What it is NOT**: Not an enterprise IT security suite, not an antivirus, not a network firewall
- **Segment**: SMB primarily, expanding to enterprise via managed security services
- **Metrics**: ~XX mNOK GP (current year), BO target: XX mNOK total
- **Source**: [security_strategy.md](../roadmap/security/security_strategy.md)

### Enterprise Security

Security solutions tailored to large corporate customers -- distinct from the SMB security platform.

- **What it is**: Identity protection, endpoint security, network traffic security for enterprise risk profiles
- **What it is NOT**: Not the SMB product rebranded for enterprise -- different pricing, scope, and compliance focus
- **Metrics**: X mNOK (current year) target: XX mNOK total
- **Source**: [value_stream_snapshot.md](value_stream_snapshot.md)

---

## Communication Solutions

### Business Communication Platform

> **STOP -- READ THIS BEFORE WRITING ANYTHING ABOUT THIS PRODUCT.**
> This platform manages **voice, unified communications, and call routing**.
> It does NOT manage subscriptions, SIM cards, or mobile data plans.
> If your text mentions "optimize subscriptions" or "billing analysis" in this context -- you are describing the wrong product.

Business telephony and unified communications platform serving XXX,XXX active users. Being transformed into an AI-native platform with real-time transcription and voice intelligence.

- **What it is**: Business telephony, unified communications, call routing, switchboard -- evolving to AI-native voice platform
- **What it is NOT**: Not a simple phone subscription, not a consumer voice service, not just call forwarding
- **Metrics**: XXX,XXX active users, BO target: XX mNOK total
- **Source**: [customer_solutions_strategy.md](../roadmap/customer_solutions/customer_solutions_strategy.md)

---

## Admin & Hardware Solutions

### Device Manager

Hardware governance and policy platform for B2B customers. Integrates policy-driven device allocation, approval flows, and budget control with HR and ERP systems.

- **What it is**: Policy management for device allocation, hardware lifecycle governance, cost allocation automation, HR/ERP integration
- **What it is NOT**: Not a subscription/SIM management tool, not a self-service portal, not an e-commerce webshop, not a billing analysis tool
- **Metrics**: XXX,XXX active users, XX enterprise customers onboarded
- **Source**: [value_stream_snapshot.md](value_stream_snapshot.md)

**An AI advisor in Device Manager would help with**: device policy optimization, hardware refresh recommendations, fleet health monitoring, return/reuse suggestions, compliance alerting for device policies -- NOT subscription or data plan optimization.

---

## How to Add a New Product

When a new product or service is introduced:

1. Add an entry to this catalog following the format above
2. Include: one-sentence definition, "What it is" bullets, "What it is NOT" bullets, key metrics, source doc link
3. Update the `updated:` date in the front-matter
4. The "What it is NOT" section is critical -- think about what an AI agent might confuse this product with
5. Add a **STOP-marker** (like the one on "Business Communication Platform" above) if misrepresentation is common or dangerous
