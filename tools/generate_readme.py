#!/usr/bin/env python3
"""
tools/generate_readme.py
Auto-generate README.md for a repo:
- top-level file/folder list
- short git log (latest commits)
- recent test/log summary (99-Logs)
- detected requirements & license
- quick usage / run commands
"""

from pathlib import Path
import subprocess
import datetime, zoneinfo
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "99-Logs"
OUT_README = ROOT / "README.md"
REQ_FILE = ROOT / "requirements.txt"
LICENSE_FILES = ["LICENSE", "LICENSE.md", "LICENSE.txt"]

def safe_cmd(cmd, cwd=ROOT, timeout=10):
    try:
        out = subprocess.check_output(cmd, cwd=str(cwd), stderr=subprocess.DEVNULL, text=True, timeout=timeout)
        return out.strip()
    except Exception:
        return None

def repo_name():
    return ROOT.name.replace("_", " ").title()

def top_level(limit=60):
    lines = []
    for p in sorted(ROOT.iterdir()):
        n = p.name
        if n.startswith(".git"):
            continue
        if p.is_dir():
            lines.append(f"- *{n}/*")
        else:
            lines.append(f"- {n}")
        if len(lines) >= limit:
            break
    return "\n".join(lines) or "- (empty)"

def last_commits(n=6):
    out = safe_cmd(["git", "log", f"--pretty=format:%h %an %ad %s", f"--date=short", f"-n{n}"])
    if not out:
        return "Git history unavailable."
    return "\n".join(f"- {L}" for L in out.splitlines())

def recent_logs(n=5):
    if not LOG_DIR.exists():
        return "No '99-Logs' folder found."
    files = sorted(LOG_DIR.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)[:n]
    if not files:
        return "No log files found."
    def fm(f): return f"- {f.name} ({datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()})"
    return "\n".join(fm(f) for f in files)

def detect_requirements():
    if not REQ_FILE.exists():
        return "No requirements.txt found."
    try:
        txt = REQ_FILE.read_text(encoding="utf-8")
        lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]
        return "\n".join(f"- {l}" for l in lines[:40]) or "requirements empty"
    except Exception:
        return "Unable to read requirements.txt"

def detect_license():
    for name in LICENSE_FILES:
        p = ROOT / name
        if p.exists():
            first = p.read_text(encoding="utf-8").splitlines()[0:4]
            return f"Found {name} — preview:\n\n\n{chr(10).join(first)}\n"
    return "No LICENSE file detected."

def quick_usage():
    lines = [
        "### Quick commands",
        "",
        "bash",
        "# create venv (one-time)",
        "python -m venv venv",
        "source venv/Scripts/activate   # Windows: venv\\Scripts\\activate",
        "pip install -r requirements.txt  # if present",
        "",
        "# run tests and save output",
        "python -m pytest -q > 99-Logs/W_latest_pytest_results.txt || true",
        "",
        "# regenerate README",
        "python tools/generate_readme.py",
        "git add README.md && git commit -m \"chore: update README.md\" && git push",
        "",
    ]
    return "\n".join(lines)

def build_readme():
    now = datetime.datetime.now(zoneinfo.ZoneInfo("UTC")).isoformat()
    sections = [
        f"# {repo_name()}",
        "",
        f"*Auto-generated snapshot* — {now}",
        "",
        "## Project overview",
        "",
        "Small projects, exercises and mini-apps created as part of the developer learning path.",
        "",
        "## Top-level files & folders",
        "",
        top_level(80),
        "",
        "## Quick links",
        "",
        "- API / Flask code: api_db.py (if present)",
        "- Package: contact_manager/ (if present)",
        "- Logs: 99-Logs/",
        "",
        "## Latest Git commits",
        "",
        last_commits(6),
        "",
        "## Recent logs (99-Logs)",
        "",
        recent_logs(6),
        "",
        "## Requirements (partial)",
        "",
        detect_requirements(),
        "",
        "## License",
        "",
        detect_license(),
        "",
        quick_usage(),
        "",
        "## Notes / Next steps",
        "",
        "- Keep secrets out of repo: use environment variables or .env (never commit).",
        "- This README is auto-generated; tweak tools/generate_readme.py to change contents."
    ]
    return "\n".join(sections)

def main():
    print("Generating README.md ...")
    content = build_readme()
    OUT_README.write_text(content, encoding="utf-8")
    print("Wrote", OUT_README)
    print("Tip: review then git add README.md && git commit -m \"chore: update README\"")

if __name__ == "__main__":
    main()