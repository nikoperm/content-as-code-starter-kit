"""Log agent activity to logs/activity.log.

Usage:
    python scripts/log_activity.py <action> <filepath> [description]

    action:   EDIT | CREATE | DELETE | ARCHIVE | REVIEW
    filepath: relative path from project root
    description: optional one-line summary

Called automatically by Claude Code hooks. Other agents (Gemini, Cursor)
should call this script directly after making changes.
"""

import datetime
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "activity.log"

AGENT_ID = os.environ.get("AGENT_ID", "agent:unknown")


def log_entry(action, filepath, description=""):
    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    rel_path = filepath
    try:
        rel_path = str(Path(filepath).relative_to(PROJECT_ROOT))
    except (ValueError, TypeError):
        pass

    entry = f"{timestamp} | {AGENT_ID} | {action} | {rel_path}"
    if description:
        entry += f" | {description}"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

    print(entry)


def main():
    if len(sys.argv) < 3:
        print("Usage: log_activity.py <action> <filepath> [description]")
        sys.exit(1)

    action = sys.argv[1].upper()
    filepath = sys.argv[2]
    description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
    log_entry(action, filepath, description)


if __name__ == "__main__":
    main()
