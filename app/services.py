from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
from math import fsum

from .repository import DataStore, get_store


def list_products(store: DataStore | None = None) -> list[dict]:
    store = store or get_store()
    return [
        {
            "id": product.id,
            "name": product.name,
            "version": product.version,
            "category": product.category,
            "description": product.description,
        }
        for product in store.products.values()
    ]


def list_changes(store: DataStore | None = None) -> list[dict]:
    store = store or get_store()
    return [
        {
            "id": change.id,
            "title": change.title,
            "status": change.status,
            "created_at": change.created_at,
            "affected_part_id": change.affected_part_id,
            "affected_part_name": store.get_node_name(change.affected_part_id),
        }
        for change in store.change_requests.values()
    ]


def _walk_bom_quantities(root_id: str, store: DataStore) -> Counter[str]:
    quantities: Counter[str] = Counter()
    queue: deque[tuple[str, int]] = deque([(root_id, 1)])

    while queue:
        parent_id, multiplier = queue.popleft()
        for edge in store.children_map.get(parent_id, []):
            child_multiplier = multiplier * edge.quantity
            quantities[edge.child_id] += child_multiplier
            if edge.child_id in store.parts and store.parts[edge.child_id].kind == "assembly":
                queue.append((edge.child_id, child_multiplier))
    return quantities


def _compliance_summary(part_ids: list[str], store: DataStore) -> dict:
    declarations: set[str] = set()
    gaps: list[dict] = []
    for part_id in part_ids:
        part = store.get_part(part_id)
        if not part:
            continue
        declarations.update(part.compliance)
        if part.compliance_gaps:
            gaps.append(
                {
                    "part_id": part.id,
                    "part_name": part.name,
                    "gaps": part.compliance_gaps,
                }
            )
    return {
        "declarations_present": sorted(declarations),
        "gaps": gaps,
    }


def _changes_for_product(product_id: str, store: DataStore) -> list[dict]:
    part_quantities = _walk_bom_quantities(product_id, store)
    part_ids = set(part_quantities.keys())
    items = []
    for change in store.change_requests.values():
        if change.affected_part_id in part_ids:
            items.append(
                {
                    "id": change.id,
                    "title": change.title,
                    "status": change.status,
                    "created_at": change.created_at,
                    "affected_part_id": change.affected_part_id,
                    "affected_part_name": store.get_node_name(change.affected_part_id),
                }
            )
    return sorted(items, key=lambda item: item["created_at"], reverse=True)


def generate_passport(product_id: str, store: DataStore | None = None) -> dict:
    store = store or get_store()
    product = store.get_product(product_id)
    if product is None:
        raise KeyError(f"Unknown product id: {product_id}")

    quantities = _walk_bom_quantities(product_id, store)
    atomic_parts = []
    software_components = []
    single_source_parts = []
    total_cost = 0.0
    total_co2 = 0.0
    total_repairability_weight = 0.0
    total_repairability_score = 0.0
    total_recycled_weight = 0.0
    total_recycled_score = 0.0

    for part_id, quantity in sorted(quantities.items()):
        part = store.get_part(part_id)
        if part is None:
            continue
        if part.kind == "assembly":
            continue
        total_cost += part.cost * quantity
        total_co2 += part.co2_kg * quantity
        if part.repairability is not None:
            total_repairability_weight += quantity
            total_repairability_score += part.repairability * quantity
        if part.recycled_content_pct is not None:
            total_recycled_weight += quantity
            total_recycled_score += part.recycled_content_pct * quantity
        if part.single_source:
            single_source_parts.append(
                {
                    "part_id": part.id,
                    "part_name": part.name,
                    "supplier": part.supplier,
                    "lead_time_days": part.lead_time_days,
                }
            )
        if part.domain == "software":
            software_components.append(
                {
                    "part_id": part.id,
                    "part_name": part.name,
                    "sbom_ref": part.sbom_ref,
                }
            )
        atomic_parts.append(
            {
                "part_id": part.id,
                "name": part.name,
                "quantity": quantity,
                "domain": part.domain,
                "supplier": part.supplier,
                "cost": round(part.cost, 2),
                "lead_time_days": part.lead_time_days,
                "co2_kg": round(part.co2_kg, 2),
            }
        )

    repairability_score = (
        round(total_repairability_score / total_repairability_weight, 2)
        if total_repairability_weight
        else None
    )
    recycled_content_pct = (
        round(total_recycled_score / total_recycled_weight, 2)
        if total_recycled_weight
        else None
    )

    compliance = _compliance_summary(list(quantities.keys()), store)

    return {
        "passport_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": {
            "id": product.id,
            "name": product.name,
            "version": product.version,
            "category": product.category,
            "description": product.description,
        },
        "lifecycle_profile": {
            "service_life_years": product.service_life_years,
            "warranty_months": product.warranty_months,
            "end_of_life_strategy": product.end_of_life_strategy,
        },
        "bom_summary": {
            "node_count": len(quantities),
            "atomic_part_count": len(atomic_parts),
            "total_estimated_material_cost_usd": round(total_cost, 2),
            "total_estimated_embodied_carbon_kg": round(total_co2, 2),
            "average_repairability_score": repairability_score,
            "average_recycled_content_pct": recycled_content_pct,
        },
        "supply_chain": {
            "single_source_parts": single_source_parts,
            "max_component_lead_time_days": max(
                [
                    store.get_part(part_id).lead_time_days
                    for part_id in quantities
                    if store.get_part(part_id) and store.get_part(part_id).kind == "component"
                ],
                default=0,
            ),
        },
        "compliance": compliance,
        "software_components": software_components,
        "recent_change_activity": _changes_for_product(product_id, store),
        "components": atomic_parts,
        "qr_target": f"/passport/{product.id}",
    }


def find_affected_products(part_id: str, store: DataStore | None = None) -> list[dict]:
    store = store or get_store()
    if part_id not in store.parts:
        raise KeyError(f"Unknown part id: {part_id}")

    affected_product_ids: set[str] = set()
    queue = deque([part_id])
    visited = {part_id}

    while queue:
        current = queue.popleft()
        for edge in store.parent_map.get(current, []):
            parent_id = edge.parent_id
            if parent_id in visited:
                continue
            visited.add(parent_id)
            if parent_id in store.products:
                affected_product_ids.add(parent_id)
            else:
                queue.append(parent_id)

    return [
        {
            "product_id": product_id,
            "product_name": store.get_node_name(product_id),
            "version": store.products[product_id].version,
        }
        for product_id in sorted(affected_product_ids)
    ]


def analyze_change(change_id: str, store: DataStore | None = None) -> dict:
    store = store or get_store()
    change = store.change_requests.get(change_id)
    if change is None:
        raise KeyError(f"Unknown change id: {change_id}")

    current = store.get_part(change.affected_part_id)
    if current is None:
        raise KeyError(f"Unknown affected part id: {change.affected_part_id}")

    proposed = change.proposed_replacement
    affected_products = find_affected_products(change.affected_part_id, store)
    current_gaps = set(current.compliance_gaps)
    current_compliance = set(current.compliance)
    proposed_compliance = set(proposed.get("compliance", []))

    lead_time_improvement = current.lead_time_days - int(proposed.get("lead_time_days", current.lead_time_days))
    cost_delta = round(float(proposed.get("cost", current.cost)) - current.cost, 2)
    single_source_reduction = current.single_source and not bool(proposed.get("single_source", current.single_source))
    compliance_resolved = bool(current_gaps) and proposed_compliance.issuperset(current_compliance.union({"REACH"}))

    blast_radius_score = min(len(affected_products) * 15, 30)
    supply_risk_score = min(current.lead_time_days // 2, 25)
    compliance_score = 25 if current_gaps else 0
    single_source_score = 20 if current.single_source else 0
    total_priority = min(blast_radius_score + supply_risk_score + compliance_score + single_source_score, 100)

    return {
        "change": {
            "id": change.id,
            "title": change.title,
            "status": change.status,
            "created_at": change.created_at,
            "reason": change.reason,
            "notes": change.notes,
        },
        "current_part": {
            "id": current.id,
            "name": current.name,
            "supplier": current.supplier,
            "cost": current.cost,
            "lead_time_days": current.lead_time_days,
            "single_source": current.single_source,
            "compliance": current.compliance,
            "compliance_gaps": list(current_gaps),
        },
        "proposed_replacement": proposed,
        "affected_products": affected_products,
        "delta": {
            "lead_time_improvement_days": lead_time_improvement,
            "cost_delta_usd": cost_delta,
            "single_source_reduction": single_source_reduction,
            "compliance_resolved": compliance_resolved,
        },
        "priority_score": {
            "total": total_priority,
            "blast_radius": blast_radius_score,
            "supply_risk": supply_risk_score,
            "compliance": compliance_score,
            "single_source": single_source_score,
        },
    }


def overview_metrics(store: DataStore | None = None) -> dict:
    store = store or get_store()
    all_products = list(store.products.keys())
    passports = [generate_passport(product_id, store) for product_id in all_products]
    total_cost = fsum(item["bom_summary"]["total_estimated_material_cost_usd"] for item in passports)
    total_co2 = fsum(item["bom_summary"]["total_estimated_embodied_carbon_kg"] for item in passports)
    open_changes = [change for change in store.change_requests.values() if change.status != "closed"]
    return {
        "products": len(store.products),
        "parts": len(store.parts),
        "open_changes": len(open_changes),
        "aggregate_demo_cost_usd": round(total_cost, 2),
        "aggregate_demo_embodied_carbon_kg": round(total_co2, 2),
    }
