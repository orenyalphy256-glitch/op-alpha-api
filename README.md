# 02-Python

*Auto-generated snapshot* — 2025-11-11T14:42:46.523987+00:00

## Project overview

Small projects, exercises and mini-apps created as part of the developer learning path.

## Top-level files & folders

- *.pytest_cache/*
- *.vscode/*
- *99-Logs/*
- __init__.py
- *__pycache__/*
- api.log
- api_client.py
- api_db.py
- API_README.txt
- api_validated.py
- *contact_manager/*
- contacts.db
- *data/*
- export_contacts.py
- export_scheduler.py
- import_contacts.py
- README.md
- requirements.txt
- *templates/*
- *tools/*
- *venv/*

## Quick links

- API / Flask code: api_db.py (if present)
- Package: contact_manager/ (if present)
- Logs: 99-Logs/

## Latest Git commits

- 2ff1be9 Alphonce Liguori 2025-11-10 Ignore .env secrets
- fd73c10 Alphonce Liguori 2025-11-10 Ignore .env secrets
- 50fa7a2 Alphonce Liguori 2025-11-10 Re-add cleaned version without exposed key
- 809d587 Alphonce Liguori 2025-11-10 Remove sensitive API key from repo index
- 8c64e85 Alphonce Liguori 2025-11-10 Re-add cleaned version without exposed key
- a2262ca Alphonce Liguori 2025-11-10 Remove sensitive API key from repo index

## Recent logs (99-Logs)

- api.log (2025-11-10T01:02:46.639370)
- W6D53_pytest_results.txt (2025-11-10T00:32:06.195400)
- contacts_export.csv (2025-11-06T18:31:22.708530)

## Requirements (partial)

- annotated-types==0.7.0
- APScheduler==3.11.0
- beautifulsoup4==4.14.2
- blinker==1.9.0
- certifi==2025.10.5
- charset-normalizer==3.4.4
- click==8.3.0
- colorama==0.4.6
- -e git+https://github.com/orenyalphy256-glitch/op-alpha-advanced-python.git@b4b52d4eb8e0918923dda5ae9526477d8ccb602f#egg=contact_manager
- Flask==3.1.2
- idna==3.11
- iniconfig==2.3.0
- itsdangerous==2.2.0
- Jinja2==3.1.6
- MarkupSafe==3.0.3
- packaging==25.0
- pluggy==1.6.0
- pydantic==2.12.3
- pydantic_core==2.41.4
- Pygments==2.19.2
- pytest==8.4.2
- requests==2.32.5
- setuptools==80.9.0
- soupsieve==2.8
- typing-inspection==0.4.2
- typing_extensions==4.15.0
- tzdata==2025.2
- tzlocal==5.3.1
- urllib3==2.5.0
- Werkzeug==3.1.3

## License

No LICENSE file detected.

### Quick commands

bash
# create venv (one-time)
python -m venv venv
source venv/Scripts/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt  # if present

# run tests and save output
python -m pytest -q > 99-Logs/W_latest_pytest_results.txt || true

# regenerate README
python tools/generate_readme.py
git add README.md && git commit -m "chore: update README.md" && git push


## Notes / Next steps

- Keep secrets out of repo: use environment variables or .env (never commit).
- This README is auto-generated; tweak tools/generate_readme.py to change contents.