#!/usr/bin/env python3
"""Telegrafen design compliance validator.

Scans HTML files, build scripts, and PPTX outputs for violations
of the Telenor Telegrafen design system.
"""
import os
import re
import sys
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_COLORS = {
    "#00193C": "#070452 or #1C16C5",
    "#001940": "#070452 or #1C16C5",
    "#00193c": "#070452 or #1C16C5",
    "#00A9E0": "#00C8FF",
    "#00a9e0": "#00C8FF",
    "#0b132b": "#070452",
    "#0B132B": "#070452",
    "#1c2541": "#0e0a6b or #1C16C5",
    "#1C2541": "#0e0a6b or #1C16C5",
    "#48cae4": "#00C8FF",
    "#48CAE4": "#00C8FF",
    "#00b4d8": "#00C8FF",
    "#00B4D8": "#00C8FF",
}

FORBIDDEN_FONTS = ["Outfit", "Inter"]

UNSAFE_CSS_PATTERNS = [
    (r"background-clip:\s*text", "background-clip: text causes PDF rendering artifacts"),
    (r"-webkit-background-clip:\s*text", "-webkit-background-clip: text causes PDF rendering artifacts"),
    (r"-webkit-text-fill-color:\s*transparent", "gradient text not supported in print"),
]

SCAN_DIRS = [
    os.path.join(PROJECT_ROOT, "build"),
    os.path.join(PROJECT_ROOT, "scripts"),
]

SCAN_EXTENSIONS = {".html", ".css", ".py"}

IGNORE_PATTERNS = [".venv", "node_modules", "__pycache__"]


def scan_file(filepath):
    errors = []
    warnings = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception:
        return errors, warnings

    rel_path = os.path.relpath(filepath, PROJECT_ROOT)
    is_html = filepath.endswith(".html")
    is_css = filepath.endswith(".css")
    is_py = filepath.endswith(".py")

    for line_num, line in enumerate(lines, 1):
        for forbidden, replacement in FORBIDDEN_COLORS.items():
            if forbidden in line:
                stripped = line.strip()
                if is_py and stripped.startswith("#") and not stripped.startswith("#0"):
                    continue
                errors.append(
                    f"  ERROR  {rel_path}:{line_num} — Forbidden color {forbidden} "
                    f"(use {replacement})"
                )

        for font in FORBIDDEN_FONTS:
            pattern = rf"(?<![a-zA-Z]){font}(?![a-zA-Z])"
            if re.search(pattern, line) and "validate_design" not in rel_path:
                errors.append(
                    f"  ERROR  {rel_path}:{line_num} — Forbidden font '{font}' "
                    f"(use 'DM Sans')"
                )

        if is_html or is_css:
            for pattern, msg in UNSAFE_CSS_PATTERNS:
                if re.search(pattern, line):
                    errors.append(
                        f"  ERROR  {rel_path}:{line_num} — {msg}"
                    )

    if is_html:
        if "DM Sans" not in content and "DM+Sans" not in content:
            if "telegrafen.css" not in content:
                warnings.append(
                    f"  WARN   {rel_path} — Missing DM Sans font import"
                )

    return errors, warnings


def main():
    all_errors = []
    all_warnings = []
    files_scanned = 0

    for scan_dir in SCAN_DIRS:
        if not os.path.exists(scan_dir):
            continue
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_PATTERNS]
            for filename in files:
                if filename == "validate_design.py":
                    continue
                ext = os.path.splitext(filename)[1]
                if ext not in SCAN_EXTENSIONS:
                    continue
                filepath = os.path.join(root, filename)
                errors, warnings = scan_file(filepath)
                all_errors.extend(errors)
                all_warnings.extend(warnings)
                files_scanned += 1

    print(f"Telegrafen Design Compliance — scanned {files_scanned} files")
    print(f"{'=' * 60}")

    if all_errors:
        print(f"\n{len(all_errors)} ERROR(s):")
        for err in all_errors:
            print(err)

    if all_warnings:
        print(f"\n{len(all_warnings)} WARNING(s):")
        for warn in all_warnings:
            print(warn)

    if not all_errors and not all_warnings:
        print("\nAll checks passed. Design is Telegrafen-compliant.")

    print(f"\nSummary: {len(all_errors)} errors, {len(all_warnings)} warnings")

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
