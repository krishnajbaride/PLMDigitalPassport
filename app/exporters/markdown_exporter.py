"""
Phase v0.2 - Markdown Exporter Module
Exports change impact analysis as formatted Markdown reports
"""

from typing import List, Dict, Any
from datetime import datetime


class MarkdownExporter:
    """Export change impact analysis to Markdown format"""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
    
    def export_impact_analysis(self, 
                              change_order: Dict[str, Any],
                              affected_products: List[Dict[str, Any]],
                              impact_details: Dict[str, Any]) -> str:
        """
        Generate a comprehensive Markdown report for change impact analysis
        
        Args:
            change_order: ECO/Change order data
            affected_products: List of products affected by the change
            impact_details: Detailed impact analysis
            
        Returns:
            Formatted Markdown string
        """
        
        md = []
        
        # Header
        md.append("# Change Impact Analysis Report")
        md.append("")
        md.append(f"**Generated:** {self.timestamp}")
        md.append("")
        
        # Change Order Summary
        md.append("## Change Order Summary")
        md.append("")
        md.append(f"- **Change ID:** {change_order.get('id', 'N/A')}")
        md.append(f"- **Title:** {change_order.get('title', 'N/A')}")
        md.append(f"- **Description:** {change_order.get('description', 'N/A')}")
        md.append(f"- **Priority:** {change_order.get('priority', 'Medium')}")
        md.append(f"- **Status:** {change_order.get('status', 'Pending')}")
        md.append(f"- **Proposed Change:** {change_order.get('change_description', 'N/A')}")
        md.append("")
        
        # Impact Summary
        md.append("## Impact Summary")
        md.append("")
        md.append(f"- **Total Affected Products:** {len(affected_products)}")
        md.append(f"- **Critical Impact:** {impact_details.get('critical_count', 0)} product(s)")
        md.append(f"- **High Impact:** {impact_details.get('high_count', 0)} product(s)")
        md.append(f"- **Medium Impact:** {impact_details.get('medium_count', 0)} product(s)")
        md.append(f"- **Low Impact:** {impact_details.get('low_count', 0)} product(s)")
        md.append("")
        
        # Affected Products Table
        md.append("## Affected Products")
        md.append("")
        md.append("| Product | SKU | Impact Level | Reason | Action Required |")
        md.append("|---------|-----|--------------|--------|-----------------|")
        
        for product in affected_products:
            md.append(
                f"| {product.get('name', 'N/A')} | {product.get('sku', 'N/A')} | "
                f"{product.get('impact_level', 'Unknown')} | "
                f"{product.get('impact_reason', 'N/A')} | "
                f"{product.get('action_required', 'Review')} |"
            )
        
        md.append("")
        
        # Detailed Impact Analysis
        md.append("## Detailed Impact Analysis")
        md.append("")
        
        if impact_details.get('affected_components'):
            md.append("### Affected Components")
            md.append("")
            for component in impact_details['affected_components']:
                md.append(f"**{component.get('part_number', 'N/A')}**")
                md.append(f"- Name: {component.get('name', 'N/A')}")
                md.append(f"- Current Supplier: {component.get('supplier', 'N/A')}")
                md.append(f"- Proposed Change: {component.get('proposed_change', 'N/A')}")
                md.append(f"- Affected Quantities: {component.get('quantity_affected', 0)}")
                md.append("")
        
        # Compliance and Sustainability Impact
        md.append("### Compliance & Sustainability Impact")
        md.append("")
        
        compliance = impact_details.get('compliance_impact', {})
        if compliance:
            md.append(f"- **RoHS Status:** {compliance.get('rohs', 'N/A')}")
            md.append(f"- **REACH Compliance:** {compliance.get('reach', 'N/A')}")
            md.append(f"- **Carbon Impact:** {compliance.get('carbon_impact', 'N/A')}")
            md.append(f"- **Material Impact:** {compliance.get('material_impact', 'N/A')}")
            md.append("")
        
        # Risk Assessment
        md.append("### Risk Assessment")
        md.append("")
        
        risks = impact_details.get('risks', [])
        if risks:
            for i, risk in enumerate(risks, 1):
                md.append(f"**Risk {i}:** {risk.get('description', 'N/A')}")
                md.append(f"- Probability: {risk.get('probability', 'Unknown')}")
                md.append(f"- Impact: {risk.get('impact', 'Unknown')}")
                md.append(f"- Mitigation: {risk.get('mitigation', 'N/A')}")
                md.append("")
        else:
            md.append("No critical risks identified.")
            md.append("")
        
        # Recommendations
        md.append("## Recommendations")
        md.append("")
        
        recommendations = impact_details.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                md.append(f"{i}. {rec}")
                md.append("")
        else:
            md.append("No specific recommendations at this time.")
            md.append("")
        
        # Cost Impact
        md.append("## Cost Impact Analysis")
        md.append("")
        
        cost = impact_details.get('cost_impact', {})
        if cost:
            md.append(f"- **Unit Cost Change:** {cost.get('unit_cost_change', 'N/A')}")
            md.append(f"- **Total Annual Impact:** {cost.get('annual_impact', 'N/A')}")
            md.append(f"- **One-time Costs:** {cost.get('one_time_costs', 'N/A')}")
            md.append("")
        
        # Timeline
        md.append("## Implementation Timeline")
        md.append("")
        
        timeline = impact_details.get('timeline', {})
        if timeline:
            md.append(f"- **Design Review:** {timeline.get('design_review', 'N/A')}")
            md.append(f"- **Procurement:** {timeline.get('procurement', 'N/A')}")
            md.append(f"- **Testing:** {timeline.get('testing', 'N/A')}")
            md.append(f"- **Implementation:** {timeline.get('implementation', 'N/A')}")
            md.append(f"- **Full Deployment:** {timeline.get('full_deployment', 'N/A')}")
            md.append("")
        
        # Affected Stakeholders
        md.append("## Affected Stakeholders")
        md.append("")
        
        stakeholders = impact_details.get('stakeholders', [])
        if stakeholders:
            for stakeholder in stakeholders:
                md.append(f"- **{stakeholder.get('role', 'N/A')}:** {stakeholder.get('action', 'Review required')}")
                md.append("")
        
        # Footer
        md.append("---")
        md.append("")
        md.append("*This report was automatically generated by ThreadPass PLM*")
        md.append(f"*Report ID: {change_order.get('id', 'N/A')}-{self.timestamp.split('T')[0]}*")
        
        return "\n".join(md)
    
    def export_supplier_impact(self, 
                              supplier_changes: List[Dict[str, Any]],
                              affected_products: List[Dict[str, Any]]) -> str:
        """
        Export supplier-specific impact analysis
        
        Args:
            supplier_changes: List of supplier changes
            affected_products: Products affected by supplier changes
            
        Returns:
            Formatted Markdown string
        """
        
        md = []
        
        md.append("# Supplier Impact Analysis")
        md.append("")
        md.append(f"**Generated:** {self.timestamp}")
        md.append("")
        
        md.append("## Summary")
        md.append("")
        md.append(f"- **Total Supplier Changes:** {len(supplier_changes)}")
        md.append(f"- **Affected Products:** {len(affected_products)}")
        md.append("")
        
        md.append("## Supplier Changes")
        md.append("")
        md.append("| Component | Current Supplier | New Supplier | Lead Time | Risk |")
        md.append("|-----------|------------------|--------------|-----------|------|")
        
        for change in supplier_changes:
            md.append(
                f"| {change.get('component', 'N/A')} | "
                f"{change.get('current_supplier', 'N/A')} | "
                f"{change.get('new_supplier', 'N/A')} | "
                f"{change.get('lead_time', 'N/A')} weeks | "
                f"{change.get('risk_level', 'Medium')} |"
            )
        
        md.append("")
        
        md.append("## Affected Products")
        md.append("")
        for product in affected_products:
            md.append(f"- **{product.get('name', 'N/A')}** ({product.get('sku', 'N/A')})")
            md.append(f"  - Affected Components: {len(product.get('affected_components', []))}")
            md.append(f"  - Recommendation: {product.get('recommendation', 'Verify compatibility')}")
            md.append("")
        
        md.append("---")
        md.append("*Supplier analysis report from ThreadPass PLM*")
        
        return "\n".join(md)
    
    def export_bom_comparison(self, 
                              product_name: str,
                              current_bom: Dict[str, Any],
                              proposed_bom: Dict[str, Any]) -> str:
        """
        Export BOM comparison report
        
        Args:
            product_name: Name of the product
            current_bom: Current BOM details
            proposed_bom: Proposed BOM details
            
        Returns:
            Formatted Markdown string
        """
        
        md = []
        
        md.append(f"# BOM Comparison Report - {product_name}")
        md.append("")
        md.append(f"**Generated:** {self.timestamp}")
        md.append("")
        
        md.append("## Overview")
        md.append("")
        md.append(f"- **Product:** {product_name}")
        md.append(f"- **Current BOM Version:** {current_bom.get('version', 'N/A')}")
        md.append(f"- **Proposed BOM Version:** {proposed_bom.get('version', 'N/A')}")
        md.append("")
        
        md.append("## Summary Statistics")
        md.append("")
        current_parts = current_bom.get('parts', [])
        proposed_parts = proposed_bom.get('parts', [])
        
        md.append(f"- **Current Parts Count:** {len(current_parts)}")
        md.append(f"- **Proposed Parts Count:** {len(proposed_parts)}")
        md.append(f"- **Components Added:** {len([p for p in proposed_parts if p not in current_parts])}")
        md.append(f"- **Components Removed:** {len([p for p in current_parts if p not in proposed_parts])}")
        md.append("")
        
        md.append("## Changes")
        md.append("")
        md.append("| Part Number | Description | Change Type | Impact |")
        md.append("|-------------|-------------|-------------|--------|")
        
        all_part_nums = set(p.get('part_number') for p in current_parts + proposed_parts)
        for part_num in sorted(all_part_nums):
            current = next((p for p in current_parts if p.get('part_number') == part_num), None)
            proposed = next((p for p in proposed_parts if p.get('part_number') == part_num), None)
            
            if current and not proposed:
                md.append(f"| {part_num} | {current.get('description', 'N/A')} | Removed | Material |")
            elif proposed and not current:
                md.append(f"| {part_num} | {proposed.get('description', 'N/A')} | Added | New |")
            elif current and proposed and current != proposed:
                md.append(f"| {part_num} | {proposed.get('description', 'N/A')} | Modified | Update |")
        
        md.append("")
        md.append("---")
        md.append("*BOM comparison report from ThreadPass PLM*")
        
        return "\n".join(md)
