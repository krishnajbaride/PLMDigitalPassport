"""
Pytest configuration and shared fixtures
"""
from __future__ import annotations

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def client():
    """
    FastAPI test client
    
    Usage:
        def test_endpoint(client):
            response = client.get("/api/v1/endpoint")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
def sample_part():
    """Sample part data for testing"""
    return {
        "part_number": "TEST-001",
        "description": "Test Part",
        "category": "Test",
        "supplier": "Test Supplier",
        "quantity": 10,
        "cost": 5.50
    }


@pytest.fixture
def sample_bom():
    """Sample BOM data for testing"""
    return {
        "name": "Test BOM",
        "version": "1.0",
        "parts": [
            {
                "part_number": "R001",
                "description": "Resistor",
                "quantity": 100,
                "supplier": "Mouser"
            },
            {
                "part_number": "C001",
                "description": "Capacitor",
                "quantity": 50,
                "supplier": "Digi-Key"
            }
        ]
    }


@pytest.fixture
def sample_change_order():
    """Sample ECO (Engineering Change Order) data"""
    return {
        "eco_number": "ECO-2024-001",
        "title": "Supplier Change",
        "description": "Changing supplier for R001",
        "priority": "medium",
        "status": "draft",
        "affected_parts": ["R001"]
    }


@pytest.fixture
def auth_headers():
    """
    Headers with authentication token
    
    Note: Implement when auth is added in v0.4
    """
    return {
        "Authorization": "Bearer test-token-placeholder"
    }
