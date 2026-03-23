# ThreadPass PLM

**ThreadPass PLM** is a composable, open-source starter project for **product lifecycle management (PLM)** that focuses on a gap many traditional tools do not expose well in a lightweight repo: **graph-style engineering change impact analysis + digital product passport generation from BOM data**.

Instead of trying to rebuild an entire enterprise PLM suite, this project gives you a clean, GitHub-friendly starter that demonstrates:

- hybrid **BOM-aware** lifecycle modeling
- **engineering change impact** analysis across shared components
- **digital product passport** generation for a product and its lifecycle metadata
- basic support for **software traceability** through SBOM-style references
- a small web UI, REST API, CLI, tests, Docker support, and GitHub Actions CI

## Why this project stands out

Existing PLM tools already cover core document, BOM, revision, and ECO workflows. For example, **openPLM** highlights BOM creation, revisions, document links, and traceability, while **Odoo PLM** documents ECO workflows and BOM revision handling. The opportunity for a distinctive GitHub project is to build something narrower and more modern: a **composable service** that sits beside PLM data and turns it into actionable lifecycle insights, especially around product passports, sustainability, traceability, and blast-radius analysis.

That is what ThreadPass PLM does.

## Project concept

This repo models three demo products that share assemblies and parts. When a high-risk part changes, the app calculates:

- which products are affected
- the blast radius of the change
- lead-time improvement or regression
- single-source risk reduction
- basic compliance gap resolution

It also generates a **Digital Product Passport JSON** for each product, including:

- lifecycle profile
- cost and embodied carbon rollups
- recycled-content and repairability indicators
- software component references
- recent engineering change activity
- single-source supplier hotspots

## Tech stack

- **Python 3.11**
- **FastAPI** for the backend API
- **Vanilla HTML/CSS/JS** for the lightweight demo UI
- **Pytest** for tests
- **Docker** and **docker-compose** for easy startup
- **GitHub Actions** for CI

## Repo structure

```text
threadpass-plm/
├── app/
│   ├── main.py
│   ├── cli.py
│   ├── repository.py
│   ├── schemas.py
│   ├── services.py
│   └── static/
├── data/
│   ├── boms.json
│   ├── changes.json
│   ├── parts.json
│   └── products.json
├── docs/
├── tests/
├── .github/
├── Dockerfile
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Quick start

### Option 1: Local Python setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/` for the UI
- `http://127.0.0.1:8000/docs` for Swagger/OpenAPI docs

### Option 2: Docker

```bash
docker compose up --build
```

## CLI examples

List demo products:

```bash
python -m app.cli products
```

Generate a digital passport:

```bash
python -m app.cli passport PRD-100
```

Analyze a proposed change:

```bash
python -m app.cli impact ECO-101
```

## REST API examples

List products:

```bash
curl http://127.0.0.1:8000/api/products
```

Generate a passport:

```bash
curl http://127.0.0.1:8000/api/passports/PRD-100
```

Analyze change impact:

```bash
curl http://127.0.0.1:8000/api/impact/ECO-101
```

## Why this is relevant now

This repo is designed around current PLM themes:

- **Digital Product Passports (DPPs)** are becoming strategically important under the EU’s Ecodesign for Sustainable Products Regulation.
- **Composable and graph-connected PLM** ideas are growing because many teams do not want a monolithic PLM rewrite just to unlock better traceability.
- **Hybrid BOM thinking** is increasingly important as physical products also carry software and SBOM-like requirements.

## Suggested GitHub repository metadata

**Repository name**

`threadpass-plm`

**Description**

`Composable open-source PLM starter for digital product passports and engineering change impact analysis.`

**Topics**

`plm`, `product-lifecycle-management`, `digital-thread`, `bom`, `engineering-change`, `digital-product-passport`, `fastapi`, `manufacturing`, `supply-chain`, `sbom`

## Customization ideas before you publish

1. Replace the demo product names with your own industry scenario.
2. Update `CITATION.cff` with your name.
3. Add screenshots or a GIF after running the UI locally.
4. Expand the data model with suppliers, quality events, service tickets, or end-of-life workflows.
5. Add CSV upload and export so recruiters and reviewers can try it without editing JSON.

## Roadmap

- CSV/Excel BOM import
- product passport export as signed JSON-LD
- graph visualization of part-to-product blast radius
- supplier risk scoring using external feeds
- authentication and write APIs
- sector templates for electronics, machinery, and consumer goods

## License

MIT
