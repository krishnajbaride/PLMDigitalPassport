"""
Phase v0.3 - Scenario Comparison Module
Compare current vs proposed BOMs
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class BOMLevelComparison:
    """Comparison at BOM level"""
    current_version: str
    proposed_version: str
    current_part_count: int
    proposed_part_count: int
    added_parts: List[Dict[str, Any]]
    removed_parts: List[Dict[str, Any]]
    modified_parts: List[Dict[str, Any]]
    unchanged_parts: List[Dict[str, Any]]


class ScenarioComparator:
    """Compare current and proposed BOMs for change scenarios"""
    
    def compare_boms(self, 
                    current_bom: Dict[str, Any],
                    proposed_bom: Dict[str, Any]) -> BOMLevelComparison:
        """
        Compare two BOMs and identify differences
        
        Args:
            current_bom: Current BOM
            proposed_bom: Proposed BOM
            
        Returns:
            BOMLevelComparison object with detailed comparisons
        """
        current_parts = current_bom.get('parts', [])
        proposed_parts = proposed_bom.get('parts', [])
        
        # Create lookup dictionaries
        current_lookup = {p.get('part_number'): p for p in current_parts}
        proposed_lookup = {p.get('part_number'): p for p in proposed_parts}
        
        # Identify changes
        added_parts = []
        removed_parts = []
        modified_parts = []
        unchanged_parts = []
        
        # Check for added and modified parts
        for part_num, proposed_part in proposed_lookup.items():
            if part_num not in current_lookup:
                added_parts.append(proposed_part)
            elif current_lookup[part_num] != proposed_part:
                modified_parts.append({
                    "part_number": part_num,
                    "current": current_lookup[part_num],
                    "proposed": proposed_part,
                    "changes": self._identify_changes(current_lookup[part_num], proposed_part)
                })
            else:
                unchanged_parts.append(proposed_part)
        
        # Check for removed parts
        for part_num, current_part in current_lookup.items():
            if part_num not in proposed_lookup:
                removed_parts.append(current_part)
        
        return BOMLevelComparison(
            current_version=current_bom.get('version', '1.0'),
            proposed_version=proposed_bom.get('version', '2.0'),
            current_part_count=len(current_parts),
            proposed_part_count=len(proposed_parts),
            added_parts=added_parts,
            removed_parts=removed_parts,
            modified_parts=modified_parts,
            unchanged_parts=unchanged_parts
        )
    
    def _identify_changes(self,
                         current_part: Dict[str, Any],
                         proposed_part: Dict[str, Any]) -> Dict[str, Any]:
        """Identify what specific fields changed"""
        changes = {}
        
        for key in set(current_part.keys()) | set(proposed_part.keys()):
            current_val = current_part.get(key)
            proposed_val = proposed_part.get(key)
            
            if current_val != proposed_val:
                changes[key] = {
                    "from": current_val,
                    "to": proposed_val
                }
        
        return changes
    
    def estimate_impact(self, comparison: BOMLevelComparison) -> Dict[str, Any]:
        """
        Estimate impact of proposed changes
        
        Args:
            comparison: BOMLevelComparison object
            
        Returns:
            Impact assessment
        """
        total_changes = len(comparison.added_parts) + len(comparison.removed_parts) + len(comparison.modified_parts)
        change_percentage = (total_changes / max(comparison.current_part_count, 1)) * 100
        
        impact = {
            "total_changes": total_changes,
            "change_percentage": round(change_percentage, 2),
            "parts_added": len(comparison.added_parts),
            "parts_removed": len(comparison.removed_parts),
            "parts_modified": len(comparison.modified_parts),
            "parts_unchanged": len(comparison.unchanged_parts),
            "risk_level": self._assess_risk(comparison),
            "complexity_score": self._calculate_complexity(comparison),
            "recommendations": self._generate_recommendations(comparison)
        }
        
        return impact
    
    def _assess_risk(self, comparison: BOMLevelComparison) -> str:
        """Assess risk level of proposed changes"""
        total_changes = len(comparison.added_parts) + len(comparison.removed_parts) + len(comparison.modified_parts)
        
        if total_changes == 0:
            return "None"
        elif total_changes <= 3:
            return "Low"
        elif total_changes <= 10:
            return "Medium"
        elif total_changes <= 25:
            return "High"
        else:
            return "Critical"
    
    def _calculate_complexity(self, comparison: BOMLevelComparison) -> int:
        """Calculate complexity score (0-100)"""
        score = 0
        
        # Each type of change adds complexity
        score += len(comparison.added_parts) * 10
        score += len(comparison.removed_parts) * 8
        score += len(comparison.modified_parts) * 6
        
        # Normalize to 0-100
        return min(score, 100)
    
    def _generate_recommendations(self, comparison: BOMLevelComparison) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if len(comparison.added_parts) > 5:
            recommendations.append("Consider phased implementation due to high number of new components")
        
        if len(comparison.removed_parts) > 0:
            recommendations.append("Verify obsolescence strategy and inventory impact of removed parts")
        
        if len(comparison.modified_parts) > 3:
            recommendations.append("Schedule supplier qualification for modified components")
        
        if len(comparison.modified_parts) > 0:
            recommendations.append("Verify design compatibility for all modifications")
        
        if comparison.change_percentage > 30:
            recommendations.append("Consider full validation testing due to significant BOM restructuring")
        
        return recommendations
    
    def export_comparison_summary(self, comparison: BOMLevelComparison) -> str:
        """Export comparison as human-readable summary"""
        summary = f"""
BOM Scenario Comparison Summary
================================

Current Version: {comparison.current_version}
Proposed Version: {comparison.proposed_version}

Current Part Count: {comparison.current_part_count}
Proposed Part Count: {comparison.proposed_part_count}

Changes Summary:
- Parts Added: {len(comparison.added_parts)}
- Parts Removed: {len(comparison.removed_parts)}
- Parts Modified: {len(comparison.modified_parts)}
- Parts Unchanged: {len(comparison.unchanged_parts)}

Added Parts:
"""
        for part in comparison.added_parts:
            summary += f"  + {part.get('part_number')} - {part.get('description')}\n"
        
        summary += "\nRemoved Parts:\n"
        for part in comparison.removed_parts:
            summary += f"  - {part.get('part_number')} - {part.get('description')}\n"
        
        summary += "\nModified Parts:\n"
        for part_mod in comparison.modified_parts:
            summary += f"  ~ {part_mod['part_number']}\n"
            for field, change in part_mod['changes'].items():
                summary += f"    {field}: {change['from']} → {change['to']}\n"
        
        return summary
