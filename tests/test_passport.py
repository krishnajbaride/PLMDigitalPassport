from app.services import generate_passport


def test_passport_contains_expected_metrics() -> None:
    passport = generate_passport("PRD-100")

    assert passport["product"]["name"] == "AquaPulse Controller X1"
    assert passport["bom_summary"]["total_estimated_material_cost_usd"] == 86.4
    assert passport["bom_summary"]["atomic_part_count"] == 8
    assert passport["supply_chain"]["single_source_parts"][0]["part_id"] == "CMP-002"
