from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    version: str
    category: str
    description: str
    service_life_years: int
    warranty_months: int
    end_of_life_strategy: str


@dataclass(frozen=True)
class Part:
    id: str
    name: str
    kind: str
    domain: str
    supplier: str
    cost: float
    lead_time_days: int
    co2_kg: float
    repairability: float | None
    recycled_content_pct: float | None
    single_source: bool
    compliance: list[str]
    compliance_gaps: list[str]
    notes: str
    sbom_ref: str | None = None


@dataclass(frozen=True)
class BomEdge:
    parent_id: str
    child_id: str
    quantity: int


@dataclass(frozen=True)
class ChangeRequest:
    id: str
    title: str
    status: str
    created_at: str
    affected_part_id: str
    reason: list[str]
    proposed_replacement: dict[str, Any]
    notes: str
