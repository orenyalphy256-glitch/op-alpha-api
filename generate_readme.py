# generate_readme.py
# Auto-generate a README.md summarizing your project
# Usage: python generate_readme.py

import os
import datetime
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def short_git_log(n=5):
    """Return last n git commits in short form."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--pretty=oneline", f"-n{n}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or "No commit history available."
    except Exception:
        return "Git log unavailable."

def list_top_level(limit=10):
    """List top-level folders and files for quick overview."""
    lines = []
    for p in sorted(ROOT.iterdir()):
        if p.name.startswith(".git"):
            continue
        if p.is_dir():
            lines.append(f"- *{p.name}/*")
        else:
            lines.append(f"- {p.name}")
        if len(lines) >= limit:
            break
    return "\n".join(lines)

def recent_logs(log_folder="99-Logs", n=5):
    """List most recent log files."""
    p = ROOT / log_folder
    if not p.exists():
        return f"No '{log_folder}' folder found."
    files = sorted(p.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)[:n]
    if not files:
        return f"No log files found in '{log_folder}'."
    return "\n".join(
        f"- {f.name} ({datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()})"
        for f in files
    )

def build_readme():
    """Generate and write README.md."""
    title = ROOT.name.replace("_", " ").title()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    git_head = short_git_log(5)
    top = list_top_level(50)
    logs = recent_logs("99-Logs", 5)

    readme_content = f"""# {title}

*Auto-generated snapshot* — {now}

## Project Overview
This repository contains Python learning projects, CLI tools, and Flask-based mini-apps such as a contact manager.  
Use this README as a quick index of your current project contents and recent work history.

---

## Top-Level Files & Folders
{top}

---

## Recent Log Files
{logs}

---

## Latest Git Commits (Top 5)
{git_head}

---

*Generated automatically by generate_readme.py*
"""

    with open(ROOT / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("README.md updated successfully!")

if __name__ == "__main__":
    build_readme()