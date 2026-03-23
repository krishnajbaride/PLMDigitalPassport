"""
Phase v0.3 - Graph Visualization Module
Build graph structures for interactive BOM visualization
"""

from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class Node:
    """Represents a node (part/product) in the graph"""
    id: str
    label: str
    type: str  # "part", "product", "supplier"
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """Represents a relationship between nodes"""
    source: str
    target: str
    relationship_type: str  # "bom", "alternative", "supplier", "affects"
    properties: Dict[str, Any] = field(default_factory=dict)


class GraphBuilder:
    """Build graph structures from BOM data"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
    
    def add_bom_as_graph(self, 
                        product_name: str,
                        product_sku: str,
                        bom_parts: List[Dict[str, Any]]) -> None:
        """
        Convert BOM to graph structure
        
        Args:
            product_name: Product name
            product_sku: Product SKU
            bom_parts: List of parts in BOM
        """
        # Add product node
        product_node = Node(
            id=f"product_{product_sku}",
            label=product_name,
            type="product",
            properties={"sku": product_sku}
        )
        self.nodes[product_node.id] = product_node
        
        # Add part nodes and BOM relationships
        for part in bom_parts:
            part_id = f"part_{part.get('part_number', 'unknown')}"
            
            # Add part node
            part_node = Node(
                id=part_id,
                label=part.get('description', part.get('part_number', 'Unknown')),
                type="part",
                properties={
                    "part_number": part.get('part_number'),
                    "supplier": part.get('supplier'),
                    "category": part.get('category')
                }
            )
            self.nodes[part_id] = part_node
            
            # Add BOM edge (product uses part)
            bom_edge = Edge(
                source=product_node.id,
                target=part_id,
                relationship_type="bom",
                properties={"quantity": part.get('quantity', 1)}
            )
            self.edges.append(bom_edge)
            
            # Add supplier node and edge
            if part.get('supplier'):
                supplier_id = f"supplier_{part['supplier'].lower().replace(' ', '_')}"
                supplier_node = Node(
                    id=supplier_id,
                    label=part['supplier'],
                    type="supplier",
                    properties={"name": part['supplier']}
                )
                self.nodes[supplier_id] = supplier_node
                
                supplier_edge = Edge(
                    source=part_id,
                    target=supplier_id,
                    relationship_type="supplier",
                    properties={}
                )
                self.edges.append(supplier_edge)
            
            # Add alternatives if present
            if part.get('alternates'):
                for alt in part['alternates']:
                    alt_id = f"part_{alt}"
                    alt_node = Node(
                        id=alt_id,
                        label=alt,
                        type="part",
                        properties={"part_number": alt, "is_alternative": True}
                    )
                    self.nodes[alt_id] = alt_node
                    
                    alt_edge = Edge(
                        source=part_id,
                        target=alt_id,
                        relationship_type="alternative",
                        properties={}
                    )
                    self.edges.append(alt_edge)
    
    def add_change_impact(self, 
                         change_id: str,
                         affected_part: str,
                         impact_products: List[str]) -> None:
        """
        Add change impact relationships to graph
        
        Args:
            change_id: Change order ID
            affected_part: Part affected by change
            impact_products: Products affected by the change
        """
        # Add change node
        change_node = Node(
            id=f"change_{change_id}",
            label=f"Change {change_id}",
            type="change",
            properties={"change_id": change_id}
        )
        self.nodes[change_node.id] = change_node
        
        # Add edges for change -> part
        part_id = f"part_{affected_part}"
        if part_id in self.nodes:
            change_edge = Edge(
                source=change_node.id,
                target=part_id,
                relationship_type="affects",
                properties={}
            )
            self.edges.append(change_edge)
        
        # Add edges for part -> product impact
        for product in impact_products:
            product_id = f"product_{product}"
            if product_id in self.nodes:
                impact_edge = Edge(
                    source=part_id,
                    target=product_id,
                    relationship_type="impacts",
                    properties={"indirect": True}
                )
                self.edges.append(impact_edge)
    
    def get_d3_format(self) -> Dict[str, Any]:
        """
        Export graph in D3.js compatible format
        
        Returns:
            Dictionary with 'nodes' and 'links' for D3.js
        """
        nodes_list = []
        for node in self.nodes.values():
            nodes_list.append({
                "id": node.id,
                "label": node.label,
                "type": node.type,
                "properties": node.properties
            })
        
        links_list = []
        for edge in self.edges:
            links_list.append({
                "source": edge.source,
                "target": edge.target,
                "type": edge.relationship_type,
                "properties": edge.properties
            })
        
        return {
            "nodes": nodes_list,
            "links": links_list
        }
    
    def get_cytoscape_format(self) -> List[Dict[str, Any]]:
        """
        Export graph in Cytoscape.js compatible format
        
        Returns:
            List of node and edge definitions for Cytoscape
        """
        elements = []
        
        # Add nodes
        for node in self.nodes.values():
            elements.append({
                "data": {
                    "id": node.id,
                    "label": node.label,
                    "type": node.type,
                    **node.properties
                }
            })
        
        # Add edges
        for edge in self.edges:
            elements.append({
                "data": {
                    "source": edge.source,
                    "target": edge.target,
                    "type": edge.relationship_type,
                    **edge.properties
                }
            })
        
        return elements
    
    def find_impact_path(self, start_node: str, end_node: str) -> List[str]:
        """
        Find shortest path between two nodes (BFS)
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            
        Returns:
            List of node IDs representing the path
        """
        from collections import deque
        
        if start_node not in self.nodes or end_node not in self.nodes:
            return []
        
        visited = set()
        queue = deque([(start_node, [start_node])])
        
        while queue:
            current, path = queue.popleft()
            
            if current == end_node:
                return path
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Find connected nodes
            for edge in self.edges:
                if edge.source == current and edge.target not in visited:
                    queue.append((edge.target, path + [edge.target]))
        
        return []
    
    def get_impact_graph(self, affected_part: str) -> Dict[str, Any]:
        """
        Get graph showing impact of a part change
        
        Args:
            affected_part: Part that changed
            
        Returns:
            Graph data with impacted products
        """
        part_id = f"part_{affected_part}"
        impacted = {"direct": [], "indirect": []}
        visited = set()
        
        def traverse_impacts(node_id: str, level: int = 0):
            if node_id in visited:
                return
            visited.add(node_id)
            
            for edge in self.edges:
                if edge.source == node_id and edge.relationship_type in ["impacts", "bom"]:
                    target_node = self.nodes.get(edge.target)
                    if target_node:
                        if level == 0:
                            impacted["direct"].append(edge.target)
                        else:
                            impacted["indirect"].append(edge.target)
                        traverse_impacts(edge.target, level + 1)
        
        traverse_impacts(part_id)
        
        return {
            "affected_part": affected_part,
            "impacted_products": impacted,
            "total_impact_count": len(impacted["direct"]) + len(impacted["indirect"])
        }
    
    def clear(self) -> None:
        """Clear the graph"""
        self.nodes.clear()
        self.edges.clear()
