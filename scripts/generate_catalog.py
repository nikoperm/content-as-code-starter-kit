"""Generate CATALOG.md automatically from front-matter in all strategy documents.

Usage:
    python scripts/generate_catalog.py          # preview to stdout
    python scripts/generate_catalog.py --save   # overwrite CATALOG.md
"""

import os
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip install pyyaml")

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STRATEGY_DIR = PROJECT_ROOT / "strategy"
CATALOG_PATH = PROJECT_ROOT / "CATALOG.md"

DOMAIN_ORDER = [
    ("overview", "Strategy & Vision", "strategy/overview/"),
    ("current_state", "Current State", "strategy/current_state/"),
    ("transformation", "Transformation", "strategy/transformation/"),
    ("roadmap", "Roadmap", "strategy/roadmap/"),
    ("presentation", "Presentation", "strategy/presentation/"),
]

CATALOG_HEADER = """---
title: "Document Catalog"
purpose: "Living registry of every document in the Content-as-Code workspace"
status: active
version: "1.0"
created: 2026-06-12
updated: {today}
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
"""


def parse_front_matter(filepath):
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    if not text.startswith("---"):
        return None

    end = text.find("\n---", 3)
    if end == -1:
        return None

    try:
        fm = yaml.safe_load(text[3:end].strip())
        return fm if isinstance(fm, dict) else None
    except yaml.YAMLError:
        return None


def collect_documents():
    docs_by_domain = defaultdict(list)

    for md_file in sorted(STRATEGY_DIR.rglob("*.md")):
        parts = md_file.relative_to(PROJECT_ROOT).parts
        if "_archive" in parts:
            continue

        fm = parse_front_matter(md_file)
        if fm is None:
            continue

        rel_path = str(md_file.relative_to(PROJECT_ROOT))
        domain = fm.get("domain", "unknown")
        title = fm.get("title", md_file.stem.replace("_", " ").title())
        status = fm.get("status", "unknown")
        purpose = fm.get("purpose", "")

        docs_by_domain[domain].append({
            "title": title,
            "path": rel_path,
            "filename": md_file.name,
            "status": status,
            "purpose": purpose,
        })

    return docs_by_domain


def find_archived():
    archived = []
    for md_file in sorted(STRATEGY_DIR.rglob("*.md")):
        parts = md_file.relative_to(PROJECT_ROOT).parts
        if "_archive" in parts:
            rel_path = str(md_file.relative_to(PROJECT_ROOT))
            parent = str(Path(*parts[:-1]))
            archived.append({"path": rel_path, "parent": parent})
    return archived


def generate_catalog():
    import datetime
    today = datetime.date.today().isoformat()

    docs = collect_documents()
    archived = find_archived()
    lines = [CATALOG_HEADER.format(today=today)]

    for domain_key, section_title, section_path in DOMAIN_ORDER:
        domain_docs = docs.get(domain_key, [])
        if not domain_docs:
            continue

        lines.append(f"## {section_title} (`{section_path}`)\n")
        lines.append("| Document | Path | Status | Purpose |")
        lines.append("|:---------|:-----|:-------|:--------|")

        for doc in domain_docs:
            link = f"[{doc['filename']}]({doc['path']})"
            lines.append(f"| {doc['title']} | {link} | {doc['status']} | {doc['purpose']} |")

        domain_archives = [a for a in archived if a["parent"].startswith(section_path.rstrip("/"))]
        if domain_archives:
            parents = set(a["parent"] for a in domain_archives)
            lines.append(f"\n> **Archived**: {len(domain_archives)} document(s) in {', '.join(f'`{p}/`' for p in parents)}")

        lines.append("\n---\n")

    skills_dir = PROJECT_ROOT / ".agent" / "skills"
    if skills_dir.exists():
        lines.append("## Agent Skills (`.agent/skills/`)\n")
        lines.append("| Skill | Path | Purpose |")
        lines.append("|:------|:-----|:--------|")

        for skill_dir in sorted(skills_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                fm = parse_front_matter(skill_file)
                name = fm.get("name", skill_dir.name) if fm else skill_dir.name
                desc = fm.get("description", "").split(".")[0] if fm else ""
                rel = str(skill_file.relative_to(PROJECT_ROOT))
                lines.append(f"| {name.replace('-', ' ').title()} | [{rel}]({rel}) | {desc} |")

        lines.append("\n---\n")

    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate CATALOG.md from front-matter")
    parser.add_argument("--save", action="store_true", help="Overwrite CATALOG.md")
    args = parser.parse_args()

    catalog = generate_catalog()

    if args.save:
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            f.write(catalog)
        print(f"CATALOG.md regenerated ({CATALOG_PATH})")
    else:
        print(catalog)


if __name__ == "__main__":
    main()
