# Contributing

Thanks for your interest in improving ThreadPass PLM.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Contribution flow

1. Create a branch from `main`.
2. Keep changes focused and documented.
3. Add or update tests in `tests/`.
4. Run `pytest` before opening a pull request.
5. Describe the user value of the change, not just the code diff.

## Good first issues

- Add CSV import/export for BOM data
- Add authentication and write endpoints
- Add richer passport schemas for sector-specific products
- Add graph visualizations and impact heatmaps
