from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from .services import (
    analyze_change,
    generate_passport,
    list_changes,
    list_products,
    overview_metrics,
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# OpenAPI documentation configuration
app = FastAPI(
    title="ThreadPass PLM API",
    description="""
    ThreadPass PLM - A composable PLM microservice for digital product passports and change impact analysis.
    
    ## Features
    
    - **Product Management**: Manage product structures and BOMs
    - **Change Impact Analysis**: Analyze the impact of engineering changes across product portfolio
    - **Digital Passports**: Generate portable digital product passport artifacts
    - **Compliance Tracking**: Monitor product compliance and lifecycle information
    
    ## API Versioning
    
    All endpoints use `/api/v1/` prefix for future versioning support.
    
    ## Authentication
    
    Authentication will be added in v0.4. Currently all endpoints are public.
    
    ## Error Handling
    
    All errors return JSON with the following structure:
    ```json
    {
        "detail": "Error message",
        "status": 400,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    ```
    """,
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "docExpansion": "list",
        "persistAuthorization": True,
        "displayOperationId": True,
    }
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ThreadPass PLM API",
        version="0.1.0",
        description="PLM microservice for digital product passports",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_index() -> FileResponse:
    """Serve web UI dashboard"""
    return FileResponse(STATIC_DIR / "index.html")


@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health Check",
    response_description="Service health status"
)
def health() -> dict:
    """
    Check if the service is healthy and running.
    
    Returns:
        - **status**: "ok" if service is operational
    """
    return {"status": "ok"}


@app.get(
    "/api/overview",
    tags=["Dashboard"],
    summary="Get Overview Metrics",
    response_description="Dashboard metrics and summary statistics"
)
def api_overview() -> dict:
    """
    Get overall PLM metrics and dashboard information.
    
    Returns:
        - **total_products**: Number of products in system
        - **total_changes**: Number of engineering changes
        - **affected_products**: Count of products affected by changes
        - **compliance_coverage**: Percentage of products with compliance info
    """
    return overview_metrics()


@app.get(
    "/api/products",
    tags=["Products"],
    summary="List All Products",
    response_description="List of all products"
)
def api_products() -> list[dict]:
    """
    Retrieve all products in the system.
    
    Returns:
        List of products with:
        - **id**: Product ID
        - **name**: Product name
        - **sku**: SKU/Part number
        - **version**: Current BOM version
        - **parts_count**: Number of components in BOM
    """
    return list_products()


@app.get(
    "/api/changes",
    tags=["Engineering Changes"],
    summary="List All Engineering Changes",
    response_description="List of all ECOs"
)
def api_changes() -> list[dict]:
    """
    Retrieve all engineering change orders (ECOs) in the system.
    
    Returns:
        List of changes with:
        - **id**: Change ID
        - **title**: Change title
        - **status**: "draft", "approved", "implemented"
        - **affected_products**: List of product IDs affected
        - **impact_severity**: "low", "medium", "high", "critical"
    """
    return list_changes()


@app.get(
    "/api/passports/{product_id}",
    tags=["Passports"],
    summary="Generate Digital Product Passport",
    response_description="Digital product passport with compliance info"
)
def api_passport(product_id: str) -> dict:
    """
    Generate a digital product passport for a specific product.
    
    The passport contains:
    - Product information and BOM
    - Compliance and regulatory information
    - Material composition
    - Sustainability metrics
    - Change history
    
    Args:
        product_id: The product identifier (SKU or ID)
    
    Returns:
        - **product**: Product details
        - **bom**: Bill of materials
        - **compliance**: Compliance information
        - **materials**: Material composition
        - **sustainability**: Environmental metrics
    
    Raises:
        - **404**: Product not found
    
    Example:
        GET /api/passports/SKU-001
    """
    try:
        return generate_passport(product_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get(
    "/api/impact/{change_id}",
    tags=["Analysis"],
    summary="Analyze Change Impact",
    response_description="Detailed impact analysis for engineering change"
)
def api_change_impact(change_id: str) -> dict:
    """
    Analyze the impact of an engineering change across the product portfolio.
    
    Shows which products are affected and the blast radius of the change.
    
    Args:
        change_id: The change order identifier
    
    Returns:
        - **change**: Change order details
        - **affected_products**: List of affected products
        - **direct_impact**: Directly affected products
        - **indirect_impact**: Indirectly affected products
        - **impact_severity**: Overall impact level
        - **recommendations**: Suggested actions
    
    Raises:
        - **404**: Change not found
    
    Example:
        GET /api/impact/ECO-001
    """
    try:
        return analyze_change(change_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
