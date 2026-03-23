from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .services import (
    analyze_change,
    generate_passport,
    list_changes,
    list_products,
    overview_metrics,
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="ThreadPass PLM",
    description="Composable PLM starter for change impact analysis and digital product passports.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/overview")
def api_overview() -> dict:
    return overview_metrics()


@app.get("/api/products")
def api_products() -> list[dict]:
    return list_products()


@app.get("/api/changes")
def api_changes() -> list[dict]:
    return list_changes()


@app.get("/api/passports/{product_id}")
def api_passport(product_id: str) -> dict:
    try:
        return generate_passport(product_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/impact/{change_id}")
def api_change_impact(change_id: str) -> dict:
    try:
        return analyze_change(change_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
