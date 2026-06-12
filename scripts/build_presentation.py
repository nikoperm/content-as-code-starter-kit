#!/usr/bin/env python3
"""Build presentation — generates HTML, PPTX, and PDF from slide markdown.

Usage::

    python scripts/build_presentation.py [input.md] [--html] [--pptx] [--pdf] [--all]
    python scripts/build_presentation.py --list-layouts
    python scripts/build_presentation.py --list-icons
    python scripts/build_presentation.py --validate
"""
from __future__ import annotations

import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from presentation.slide_parser import parse_presentation, validate_presentation
from presentation.html_renderer import render_html
from presentation.telegrafen import (
    ALL_LAYOUTS, PPTX_LAYOUT_MAP, EXECUTIVE_LAYOUTS,
    NARRATIVE_LAYOUTS, ALLMOTE_LAYOUTS, SHARED_LAYOUTS,
)
from presentation.icon_manager import IconManager

DEFAULT_INPUT = os.path.join(
    PROJECT_ROOT, "strategy", "presentation", "demo_deck.md"
)
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "build")


def list_layouts() -> None:
    """Print all available layouts grouped by mode."""
    print("\n=== Executive-Only Layouts ===")
    for name in sorted(EXECUTIVE_LAYOUTS):
        pptx = PPTX_LAYOUT_MAP.get(name, "—")
        print(f"  {name:<25} → PPTX: {pptx}")

    print("\n=== Narrative-Only Layouts ===")
    for name in sorted(NARRATIVE_LAYOUTS):
        pptx = PPTX_LAYOUT_MAP.get(name, "—")
        print(f"  {name:<25} → PPTX: {pptx}")

    print("\n=== AllMøte-Only Layouts ===")
    for name in sorted(ALLMOTE_LAYOUTS):
        pptx = PPTX_LAYOUT_MAP.get(name, "—")
        print(f"  {name:<25} → PPTX: {pptx}")

    print("\n=== Shared Layouts (all modes) ===")
    for name in sorted(SHARED_LAYOUTS):
        pptx = PPTX_LAYOUT_MAP.get(name, "—")
        print(f"  {name:<25} → PPTX: {pptx}")

    print(f"\nTotal: {len(ALL_LAYOUTS)} layouts")


def list_icons() -> None:
    """Print all available icons grouped by category."""
    mgr = IconManager()
    categories = mgr.list_by_category()
    for cat, icons in categories.items():
        print(f"\n=== {cat} ===")
        for icon in icons:
            exists = "✓" if mgr.exists(icon) else "✗"
            print(f"  {exists} {icon}_expanded.svg")

    all_icons = mgr.list_all()
    print(f"\nTotal: {len(all_icons)} icons available")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build presentation from slide markdown"
    )
    parser.add_argument(
        "input", nargs="?", default=DEFAULT_INPUT,
        help="Source markdown file (default: strategy_presentation.md)"
    )
    parser.add_argument("--html", action="store_true", help="Generate HTML")
    parser.add_argument("--pptx", action="store_true", help="Generate PPTX")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF")
    parser.add_argument(
        "--all", action="store_true",
        help="Generate all formats (default if no format specified)"
    )
    parser.add_argument(
        "--mode", choices=["executive", "narrative", "allmote"],
        help="Override presentation mode"
    )
    parser.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help="Output directory (default: build/)"
    )
    parser.add_argument(
        "--list-layouts", action="store_true", help="List available layouts"
    )
    parser.add_argument(
        "--list-icons", action="store_true", help="List available icons"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate only, don't build"
    )

    args = parser.parse_args()

    if args.list_layouts:
        list_layouts()
        return

    if args.list_icons:
        list_icons()
        return

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    pres = parse_presentation(args.input, mode_override=args.mode)
    print(f"Parsed: {pres.title}")
    print(f"Mode: {pres.mode} | Slides: {len(pres.slides)}")

    issues = validate_presentation(pres)
    if issues:
        for issue in issues:
            print(f"  {issue}")
        errors = [i for i in issues if i.startswith("ERROR")]
        if errors:
            print(f"\n{len(errors)} error(s) found. Fix before building.")
            if not args.validate:
                sys.exit(1)

    if args.validate:
        if not issues:
            print("  Validation passed — no issues found.")
        return

    no_format = not (args.html or args.pptx or args.pdf)
    if args.all or no_format:
        args.html = True
        args.pptx = True

    os.makedirs(args.output_dir, exist_ok=True)

    basename = os.path.splitext(os.path.basename(args.input))[0]
    basename = basename.replace(" ", "_")

    if args.html:
        html_path = os.path.join(args.output_dir, f"{basename}.html")
        render_html(pres, html_path)
        size_kb = os.path.getsize(html_path) / 1024
        print(f"  HTML: {html_path} ({size_kb:.0f} KB)")

    if args.pptx:
        try:
            from presentation.pptx_renderer import render_pptx
            pptx_path = os.path.join(args.output_dir, f"{basename}.pptx")
            render_pptx(pres, pptx_path)
            size_kb = os.path.getsize(pptx_path) / 1024
            print(f"  PPTX: {pptx_path} ({size_kb:.0f} KB)")
        except ImportError as e:
            print(f"  PPTX: Skipped (python-pptx not available: {e})")
        except Exception as e:
            print(f"  PPTX: Error — {e}")

    if args.pdf:
        print("  PDF: Chrome headless export not yet implemented")

    print("\nDone.")


if __name__ == "__main__":
    main()
