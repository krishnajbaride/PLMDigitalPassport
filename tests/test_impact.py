from app.services import analyze_change


def test_change_impact_reaches_all_shared_products() -> None:
    impact = analyze_change("ECO-101")

    affected_ids = {item["product_id"] for item in impact["affected_products"]}
    assert affected_ids == {"PRD-100", "PRD-200", "PRD-300"}
    assert impact["delta"]["lead_time_improvement_days"] == 44
    assert impact["delta"]["single_source_reduction"] is True
