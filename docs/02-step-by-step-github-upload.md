# Step-by-Step GitHub Upload Guide

## 1) Rename and personalize the repo

Open these files and replace placeholders:

- `README.md`
- `CITATION.cff`
- `LICENSE` copyright line if desired
- demo names in `data/*.json` if you want a different product domain

## 2) Test locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Check:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## 3) Create a new repository on GitHub

Use these settings:

- Repository name: `threadpass-plm`
- Visibility: Public
- Initialize with README: **No**
- Add .gitignore: **No**
- Add license: **No**

This starter already includes those files.

## 4) Push the code

From the project folder:

```bash
git init
git add .
git commit -m "Initial commit: ThreadPass PLM starter"
git branch -M main
git remote add origin https://github.com/<your-username>/threadpass-plm.git
git push -u origin main
```

## 5) Add GitHub polish

After the first push:

- Add repository description
- Add topics from the README
- Pin the repo on your profile
- Enable Issues
- Enable Discussions if you want community feedback
- Add a screenshot to the README

## 6) Create a strong first release

Suggested release title:

`v0.1.0 - PLM passport and change impact starter`

Suggested release notes:

- FastAPI backend and demo dashboard
- sample BOM and ECO data
- digital product passport JSON generation
- engineering change blast-radius analysis
- CLI, tests, Docker, and CI

## 7) Open good first issues

Create these issues immediately so the repo looks active:

- Add CSV BOM import
- Add graph visualization
- Add JSON-LD passport export
- Add supplier risk feed integration
- Add authentication
