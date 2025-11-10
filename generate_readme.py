# generate_readme.py
# Simple script to generate a README.md file for a project
# Run from the command line: python generate_readme.py
import os
import datetime
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def short_git_log(n=5):
    try:
        out = subprocess.check_output(
            ["git", "log", f"--pretty=oneline", f"-n{n}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or "No commit history available."
    except Exception:
        return "Git log unavailable."
    
def list_top_level(limit=10):
    lines = []
    for p in sorted(ROOT.iterdir()):
        if p.name.startswith(".git"):
            continue
        if p.is_dir():
            lines.append(f"- **{p.name}/**")
        else:
            lines.append(f"- {p.name}")
        if len(lines) >= limit:
            break
    return "\n".join(lines)

def recent_logs(log_folder="99-Logs", n=5):
    p = ROOT / log_folder
    if not p.exists():
        return f"No '{log_folder}' folder found."
    files = sorted(p.glob("*"), keys=lambda f: f.stat().st_mtime, reverse=True)[:n]
    if not files:
        return f"No log files found in '{log_folder}'."
    return "\n".join(f"- {f.name} ({datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()})"
                        for f in files)

def build_readme():
    title = ROOT.name.replace("_", " ").title()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    git_head = short_git_log(5)
    top = list_top_level(60)
    logs = recent_logs("99-Logs", 5)

    readme_content = f"""# {title}

**Auto-generated snapshot** - {now}

## Project Overview
This repository contains Python learning projects, small CLI and Flask exercises, and a contact_manager mini-app.build_readme
Use this README as a quick index of the project's contents and recent activity.set

## Top-level files & folders
{top}

## Quick links
- API / Flask code: 'api_db.py' (if present)
- Package: 'contact_manager' (if present)
- Logs: '99-Logs/'
## Latest Git Commits (top 5)"""