"""Generate a human-readable changelog from git history.

Usage:
    python scripts/generate_changelog.py                    # last 7 days
    python scripts/generate_changelog.py --days 14          # last 14 days
    python scripts/generate_changelog.py --since 2026-05-01 # since date
    python scripts/generate_changelog.py --save             # write to CHANGELOG.md
"""

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DOMAIN_MAP = {
    "strategy/roadmap/security/": "Security",
    "strategy/roadmap/customer_solutions/": "Customer Solutions",
    "strategy/transformation/": "Transformation",
    "strategy/overview/": "Strategy & Vision",
    "strategy/presentation/": "Presentation",
    "strategy/current_state/": "Current State",
    ".agent/": "Platform",
    "scripts/": "Platform",
}

TYPE_MAP = {
    "docs:": "New content",
    "data:": "Data updates",
    "review:": "Reviews",
    "fix:": "Quality fixes",
    "feat:": "New capabilities",
    "refactor:": "Restructuring",
}


def classify_domain(filepath):
    for pattern, domain in DOMAIN_MAP.items():
        if filepath.startswith(pattern):
            return domain
    return "Other"


def classify_type(message):
    for prefix, label in TYPE_MAP.items():
        if message.startswith(prefix):
            return label
    return "Updates"


def get_commits(since_arg):
    cmd = ["git", "log", "--format=%H|%ad|%an|%s", "--date=short"]
    if since_arg:
        cmd.append(f"--since={since_arg}")
    cmd.append("--")
    cmd.append(".")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0][:8],
                "date": parts[1],
                "author": parts[2],
                "message": parts[3],
            })
    return commits


def get_changed_files(commit_hash):
    cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        return []
    return [f for f in result.stdout.strip().split("\n") if f]


def generate_changelog(since_arg, end_date="today"):
    commits = get_commits(since_arg)
    if not commits:
        return "No changes found in the specified timeframe.\n"

    domain_changes = defaultdict(list)
    authors = set()

    for commit in commits:
        authors.add(commit["author"])
        files = get_changed_files(commit["hash"])
        domains_seen = set()
        for f in files:
            domain = classify_domain(f)
            if domain not in domains_seen:
                domains_seen.add(domain)

        msg = commit["message"]
        for prefix in TYPE_MAP:
            if msg.startswith(prefix):
                msg = msg[len(prefix):].strip()
                break

        for domain in domains_seen:
            domain_changes[domain].append({
                "date": commit["date"],
                "message": msg,
            })

    start_date = since_arg or f"{commits[-1]['date']}"
    lines = [f"## Changelog: {start_date} — {end_date}\n"]

    domain_order = [
        "Security", "Customer Solutions",
        "Strategy & Vision", "Current State", "Transformation",
        "Presentation", "Platform", "Other",
    ]

    for domain in domain_order:
        if domain not in domain_changes:
            continue
        lines.append(f"\n### {domain}\n")
        for change in domain_changes[domain]:
            lines.append(f"- {change['message']}")

    lines.append(f"\n---\n*{len(commits)} commits by {len(authors)} contributor(s)*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate changelog")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--since", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--save", action="store_true", help="Write to CHANGELOG.md")
    args = parser.parse_args()

    since = args.since or f"{args.days} days ago"
    changelog = generate_changelog(since)

    if args.save:
        outpath = PROJECT_ROOT / "CHANGELOG.md"
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(changelog)
        print(f"Changelog written to {outpath}")
    else:
        print(changelog)


if __name__ == "__main__":
    main()
