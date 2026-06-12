"""Icon Manager — loads, themes, and renders Telenor SVG icons.

Handles the 56 SVG icons in reference/icons/, adjusting fill colors
based on slide theme (light vs dark background).
"""

from __future__ import annotations

import os
import re
from functools import lru_cache

from .telegrafen import ICONS_DIR, COLORS, ICON_CATEGORIES


class IconManager:
    def __init__(self, icons_dir: str | None = None):
        self.icons_dir = icons_dir or ICONS_DIR
        self._cache: dict[str, str] = {}

    def _resolve_filename(self, name: str) -> str:
        """Resolve icon name to filename, adding _expanded.svg if needed."""
        if name.endswith(".svg"):
            return name
        if not name.endswith("_expanded"):
            name = f"{name}_expanded"
        return f"{name}.svg"

    def _load_raw(self, name: str) -> str:
        """Load raw SVG content from disk."""
        filename = self._resolve_filename(name)
        if filename in self._cache:
            return self._cache[filename]

        path = os.path.join(self.icons_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Icon not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()
        self._cache[filename] = svg
        return svg

    def exists(self, name: str) -> bool:
        """Check if an icon file exists."""
        filename = self._resolve_filename(name)
        return os.path.exists(os.path.join(self.icons_dir, filename))

    def render_inline(self, name: str, size: int = 48, theme: str = "light") -> str:
        """Return SVG markup with fill adjusted for the slide theme.

        Args:
            name: Icon name (with or without _expanded.svg suffix)
            size: Render size in pixels
            theme: 'light' (dark icon on light bg), 'dark'/'statement' (light icon on dark bg)
        """
        svg = self._load_raw(name)

        fill_color = COLORS["dark_blue"] if theme == "light" else COLORS["telenor_blue"]

        svg = re.sub(
            r'width="[^"]*"',
            f'width="{size}px"',
            svg,
            count=1,
        )
        svg = re.sub(
            r'height="[^"]*"',
            f'height="{size}px"',
            svg,
            count=1,
        )

        svg = svg.replace(
            "<svg ",
            f'<svg class="tg-icon" style="width:{size}px;height:{size}px;" ',
            1,
        )

        svg = re.sub(r'fill="#[0-9a-fA-F]{3,8}"', f'fill="{fill_color}"', svg)
        svg = re.sub(r'fill="rgb\([^)]+\)"', f'fill="{fill_color}"', svg)

        return svg

    def render_for_pptx(self, name: str) -> str:
        """Return the file path for PPTX embedding.

        python-pptx can embed SVG files directly or via conversion.
        Returns the absolute path to the icon file.
        """
        filename = self._resolve_filename(name)
        path = os.path.join(self.icons_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Icon not found: {path}")
        return path

    def list_all(self) -> list[str]:
        """List all available icon names (without _expanded.svg suffix)."""
        icons = []
        for f in sorted(os.listdir(self.icons_dir)):
            if f.endswith("_expanded.svg"):
                name = f.replace("_expanded.svg", "")
                icons.append(name)
        return icons

    def list_by_category(self) -> dict[str, list[str]]:
        """Return icons grouped by semantic category."""
        return ICON_CATEGORIES.copy()
