#!/usr/bin/env bash
# Content-as-Code Starter Kit — One-command installer
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/nikoperm/content-as-code-starter-kit/main/install.sh | bash
#
# Or with a custom directory name:
#   curl -fsSL https://raw.githubusercontent.com/nikoperm/content-as-code-starter-kit/main/install.sh | bash -s -- my-strategy
#
set -euo pipefail

REPO_URL="https://github.com/nikoperm/content-as-code-starter-kit/archive/refs/heads/main.tar.gz"
DIR_NAME="${1:-content-as-code-starter-kit}"

echo ""
echo "  Content-as-Code Starter Kit"
echo "  ==========================="
echo ""

# Check prerequisites
for cmd in python3 git; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "  ERROR: '$cmd' is required but not installed."
    exit 1
  fi
done

# Check if directory already exists
if [ -d "$DIR_NAME" ]; then
  echo "  ERROR: Directory '$DIR_NAME' already exists."
  echo "  Remove it first or specify a different name:"
  echo "    curl -fsSL <url> | bash -s -- my-other-name"
  exit 1
fi

echo "  Downloading..."
TMPDIR=$(mktemp -d)
curl -fsSL "$REPO_URL" | tar xz -C "$TMPDIR"

# The tarball extracts to content-as-code-starter-kit-main/
mv "$TMPDIR/content-as-code-starter-kit-main" "$DIR_NAME"
rm -rf "$TMPDIR"

echo "  Setting up..."
cd "$DIR_NAME"

# Initialize as a fresh git repo (not connected to GitHub)
git init -q
git add -A
git commit -q -m "feat: initialize Content-as-Code workspace from starter kit"

# Set up Python environment
python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

# Generate initial catalog
.venv/bin/python scripts/generate_catalog.py --save 2>/dev/null || true

echo ""
echo "  Done! Your Content-as-Code workspace is ready."
echo ""
echo "  Next steps:"
echo "    cd $DIR_NAME"
echo "    make validate          # Check workspace health"
echo "    claude                 # Open in Claude Code"
echo "    # Or open in Cursor, Antigravity, etc."
echo ""
echo "  Try these agent commands:"
echo "    /bo-builder            # Create a Business Opportunity"
echo "    /presentation-design   # Create a presentation"
echo "    /strategy-review       # Review a strategy document"
echo "    /workspace-health      # Validate workspace integrity"
echo ""
