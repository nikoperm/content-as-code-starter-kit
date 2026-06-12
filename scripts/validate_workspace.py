"""Validate the Content-as-Code workspace.

Checks front-matter, CATALOG.md sync, file sizes, placeholders,
broken links, and more. Exit 0 if no ERRORs, 1 otherwise.

Usage:
    python validate_workspace.py              # full validation
    python validate_workspace.py --deep       # full + cross-reference checks
    python validate_workspace.py --quick --file path/to/file.md
    python validate_workspace.py --summary
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip install pyyaml")

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STRATEGY_DIR = PROJECT_ROOT / "strategy"
CATALOG_PATH = PROJECT_ROOT / "CATALOG.md"

REQUIRED_FIELDS = [
    "title", "purpose", "status", "version",
    "created", "updated", "author", "domain",
]

PLACEHOLDER_PATTERN = re.compile(
    r"\bPLACEHOLDER\b|\bTODO\b|\bXXX\b|\bTBD\b",
    re.IGNORECASE,
)

RELATIVE_LINK_PATTERN = re.compile(
    r"\[([^\]]*)\]\(([^)]+)\)",
)

CATALOG_LINK_PATTERN = re.compile(
    r"\(strategy/[^\)]+\.md\)",
)


class Issue:
    def __init__(self, severity, path, message):
        self.severity = severity
        self.path = path
        self.message = message

    def __str__(self):
        return f"{self.severity}: {self.path} — {self.message}"


def relative_path(p):
    try:
        return str(Path(p).relative_to(PROJECT_ROOT))
    except ValueError:
        return str(p)


def is_archived(path):
    return "/_archive/" in str(path) or "/_archive" == str(path).split("/")[-2] if "/" in str(path) else False


def path_in_archive(p):
    parts = Path(p).parts
    return "_archive" in parts


def parse_front_matter(filepath):
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None, None, text if 'text' in dir() else ""

    if not text.startswith("---"):
        return None, None, text

    end = text.find("\n---", 3)
    if end == -1:
        return None, None, text

    raw_yaml = text[3:end].strip()
    try:
        fm = yaml.safe_load(raw_yaml)
        if not isinstance(fm, dict):
            return None, raw_yaml, text
        return fm, raw_yaml, text
    except yaml.YAMLError:
        return None, raw_yaml, text


def collect_strategy_files():
    if not STRATEGY_DIR.exists():
        return []
    return sorted(STRATEGY_DIR.rglob("*.md"))


def check_front_matter_presence(filepath):
    issues = []
    fm, raw, _ = parse_front_matter(filepath)
    rp = relative_path(filepath)
    if raw is None:
        issues.append(Issue("ERROR", rp, "Missing YAML front-matter"))
    elif fm is None:
        issues.append(Issue("WARNING", rp, "Malformed YAML front-matter"))
    return issues, fm


def check_front_matter_completeness(filepath, fm):
    issues = []
    rp = relative_path(filepath)
    if fm is None:
        return issues
    for field in REQUIRED_FIELDS:
        val = fm.get(field)
        if val is None or val == "":
            issues.append(Issue("WARNING", rp, f"Front-matter field '{field}' is missing or empty"))
        elif isinstance(val, str) and val.strip().upper() == "TBD":
            issues.append(Issue("WARNING", rp, f"Front-matter field '{field}' is 'TBD'"))
    return issues


def check_file_size(filepath):
    issues = []
    rp = relative_path(filepath)
    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
        if len(lines) > 500:
            issues.append(Issue("WARNING", rp, f"File has {len(lines)} lines (limit 500)"))
    except Exception:
        pass
    return issues


def check_placeholders(filepath, fm):
    issues = []
    rp = relative_path(filepath)

    if fm and fm.get("status") == "archived":
        return issues

    if filepath.name == "execution_framework.md":
        return issues

    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return issues

    fm_end = 0
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_end = end + 4

    body = text[fm_end:]
    for i, line in enumerate(body.splitlines(), start=1):
        for m in PLACEHOLDER_PATTERN.finditer(line):
            word = m.group(0).upper()
            if word == "TBD":
                before = line[:m.start()]
                if before.rstrip().endswith(("://", "/", ".")):
                    continue
            issues.append(Issue(
                "WARNING", rp,
                f"Placeholder '{m.group(0)}' found (body line {i})"
            ))
    return issues


def check_catalog_sync(strategy_files):
    issues = []
    if not CATALOG_PATH.exists():
        issues.append(Issue("ERROR", "CATALOG.md", "CATALOG.md not found"))
        return issues

    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    for fp in strategy_files:
        if path_in_archive(fp):
            continue
        basename = fp.name
        rp = relative_path(fp)
        if basename not in catalog_text:
            issues.append(Issue("ERROR", rp, f"Not referenced in CATALOG.md"))

    return issues


def check_phantom_references():
    issues = []
    if not CATALOG_PATH.exists():
        return issues

    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")
    for m in CATALOG_LINK_PATTERN.finditer(catalog_text):
        link = m.group(0)[1:-1]
        target = PROJECT_ROOT / link
        if not target.exists():
            issues.append(Issue("ERROR", "CATALOG.md", f"Phantom link: {link} does not exist"))
    return issues


def check_broken_links(filepath):
    issues = []
    rp = relative_path(filepath)
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return issues

    parent = filepath.parent
    for m in RELATIVE_LINK_PATTERN.finditer(text):
        link_target = m.group(2)

        if link_target.startswith(("http://", "https://", "mailto:", "#", "file://")):
            continue
        if link_target.startswith("/"):
            continue

        clean = link_target.split("#")[0].split("?")[0]
        if not clean:
            continue

        import urllib.parse
        clean_unquoted = urllib.parse.unquote(clean)
        resolved = (parent / clean_unquoted).resolve()
        if not resolved.exists():
            issues.append(Issue("WARNING", rp, f"Broken link: {link_target}"))

    return issues


def check_roadmap_owners():
    issues = []
    pattern = STRATEGY_DIR / "roadmap" / "*" / "current_work.md"
    import glob
    for fp_str in sorted(glob.glob(str(pattern))):
        fp = Path(fp_str)
        fm, _, _ = parse_front_matter(fp)
        rp = relative_path(fp)
        if fm is None:
            continue
        owners = fm.get("owners")
        if owners is None or owners == [] or owners == "":
            issues.append(Issue("INFO", rp, "No owners defined in front-matter"))
    return issues


def _build_related_map(active_files):
    related_map = {}
    all_rel_paths = set()
    for fp in active_files:
        rp = relative_path(fp)
        all_rel_paths.add(rp)
        fm, _, _ = parse_front_matter(fp)
        related = []
        if fm and isinstance(fm.get("related"), list):
            related = [str(r) for r in fm["related"] if r]
        related_map[rp] = related
    return related_map, all_rel_paths


def check_asymmetric_related(active_files):
    issues = []
    related_map, _ = _build_related_map(active_files)

    for doc_path, related_list in related_map.items():
        for target in related_list:
            target_related = related_map.get(target, [])
            if doc_path not in target_related:
                issues.append(Issue(
                    "WARNING", doc_path,
                    f"Asymmetric related link: lists '{target}' but that document does not link back"
                ))
    return issues


def check_orphan_documents(active_files):
    issues = []
    related_map, all_rel_paths = _build_related_map(active_files)

    referenced = set()
    for doc_path, related_list in related_map.items():
        for target in related_list:
            referenced.add(target)

    for rp in sorted(all_rel_paths):
        if rp not in referenced:
            issues.append(Issue(
                "INFO", rp,
                "Orphan document: not referenced in any other document's related: field"
            ))
    return issues


def check_related_targets_exist(active_files):
    issues = []
    for fp in active_files:
        fm, _, _ = parse_front_matter(fp)
        if fm is None:
            continue
        related = fm.get("related")
        if not isinstance(related, list):
            continue
        rp = relative_path(fp)
        for target in related:
            if not target:
                continue
            target_path = PROJECT_ROOT / str(target)
            if not target_path.exists():
                issues.append(Issue(
                    "WARNING", rp,
                    f"Related link target does not exist: {target}"
                ))
    return issues


def run_full_validation(deep=False):
    all_issues = []
    strategy_files = collect_strategy_files()

    active_files = [f for f in strategy_files if not path_in_archive(f)]

    for fp in active_files:
        fm_issues, fm = check_front_matter_presence(fp)
        all_issues.extend(fm_issues)
        all_issues.extend(check_front_matter_completeness(fp, fm))

    all_issues.extend(check_catalog_sync(strategy_files))
    all_issues.extend(check_phantom_references())

    for fp in active_files:
        all_issues.extend(check_file_size(fp))

    for fp in active_files:
        fm, _, _ = parse_front_matter(fp)
        all_issues.extend(check_placeholders(fp, fm))

    for fp in active_files:
        all_issues.extend(check_broken_links(fp))

    all_issues.extend(check_roadmap_owners())

    if deep:
        all_issues.extend(check_related_targets_exist(active_files))
        all_issues.extend(check_asymmetric_related(active_files))
        all_issues.extend(check_orphan_documents(active_files))

    return all_issues


def run_quick_validation(filepath):
    fp = Path(filepath)
    if not fp.is_absolute():
        fp = PROJECT_ROOT / fp
    if not fp.exists():
        return [Issue("ERROR", relative_path(fp), "File not found")]

    all_issues = []
    fm_issues, fm = check_front_matter_presence(fp)
    all_issues.extend(fm_issues)
    all_issues.extend(check_front_matter_completeness(fp, fm))
    all_issues.extend(check_file_size(fp))
    all_issues.extend(check_placeholders(fp, fm))
    return all_issues


def print_issues(issues):
    for issue in issues:
        print(issue)


def summary_line(issues):
    errors = sum(1 for i in issues if i.severity == "ERROR")
    warnings = sum(1 for i in issues if i.severity == "WARNING")
    infos = sum(1 for i in issues if i.severity == "INFO")
    return f"Health: {errors} errors, {warnings} warnings, {infos} info"


def main():
    parser = argparse.ArgumentParser(description="Validate Content-as-Code workspace")
    parser.add_argument("--quick", action="store_true", help="Quick single-file validation")
    parser.add_argument("--deep", action="store_true", help="Full validation + cross-reference checks")
    parser.add_argument("--file", type=str, help="File to validate (used with --quick)")
    parser.add_argument("--summary", action="store_true", help="Print one-line health summary")
    args = parser.parse_args()

    if args.quick:
        if not args.file:
            parser.error("--quick requires --file <path>")
        issues = run_quick_validation(args.file)
    else:
        issues = run_full_validation(deep=args.deep)

    if args.summary:
        print(summary_line(issues))
    else:
        print_issues(issues)
        print()
        print(summary_line(issues))

    has_errors = any(i.severity == "ERROR" for i in issues)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
