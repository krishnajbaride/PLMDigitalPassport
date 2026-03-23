"""
Phase v0.3 - Implementation Guide
Graph Visualization, Scenario Analysis, and Enhanced Passports
"""

# Phase v0.3 Implementation Checklist

## 1. Graph Visualization Feature

### Components
- [x] Graph builder (`app/visualization/graph_builder.py`)
- [ ] D3.js based frontend visualization
- [ ] Cytoscape.js alternative visualization
- [ ] Interactive node/edge selection
- [ ] Zoom and pan controls
- [ ] Legend and controls panel

### Backend Tasks
- [ ] Create graph visualization API endpoint
- [ ] Implement graph traversal algorithms
- [ ] Add impact path finding
- [ ] Cache graph data for performance
- [ ] Support graph layout algorithms

### Frontend Tasks
- [ ] Select visualization library (D3.js recommended)
- [ ] Create canvas/SVG component
- [ ] Implement node coloring by type
- [ ] Add edge styling by relationship
- [ ] Create legend
- [ ] Add search/filter for nodes

### API Endpoints
```
GET /api/v1/bom/{id}/graph - Get BOM as graph (D3 format)
GET /api/v1/bom/{id}/graph/cytoscape - Get BOM as graph (Cytoscape format)
GET /api/v1/impact-path/{from}/{to} - Find impact path
GET /api/v1/part/{id}/impact/graph - Get impact graph for part
```

### Performance Considerations
- Implement graph caching
- Limit graph size for large BOMs (>5000 parts)
- Paginate graph rendering
- Use WebWorkers for graph computation

---

## 2. Scenario Comparison Feature

### Components
- [x] Scenario comparator (`app/visualization/scenario_comparator.py`)
- [ ] Comparison UI component
- [ ] Side-by-side BOM viewer
- [ ] Diff highlighting
- [ ] Impact assessment display

### Backend Tasks
- [ ] Implement BOM comparison logic (✅ done)
- [ ] Calculate change metrics
- [ ] Generate complexity score
- [ ] Risk assessment algorithm
- [ ] Recommendation engine

### Frontend Tasks
- [ ] Create BOM comparison view
- [ ] Highlight added/removed/modified parts
- [ ] Show change metrics
- [ ] Display risk/complexity scores
- [ ] Export comparison report

### API Endpoints
```
POST /api/v1/scenarios/compare - Compare two BOMs
GET /api/v1/scenarios/{id}/impact-analysis
POST /api/v1/scenarios/{id}/estimate-costs
GET /api/v1/scenarios/{id}/timeline
```

### Database Schema
```python
class Scenario(Base):
    id: int
    name: str
    description: str
    product_id: int
    current_bom_id: int
    proposed_bom_id: int
    created_at: datetime
    comparison_data: JSON  # Store comparison results
    risk_level: str
    complexity_score: int
```

---

## 3. Enhanced Digital Passport

### Features
- [ ] Richer passport profile
- [ ] QR code generation
- [ ] Passport versioning
- [ ] Compliance metadata
- [ ] Sustainability tracking
- [ ] Material composition
- [ ] Lifecycle stage

### Components
- [ ] QR code generator (`app/utilities/qr_generator.py`)
- [ ] Passport template engine
- [ ] Passport version management

### Backend Tasks
- [ ] Extend Passport schema
- [ ] Add QR code generation
- [ ] Create passport versioning
- [ ] Add compliance fields
- [ ] Implement passport validation

### Frontend Tasks
- [ ] Create passport viewer
- [ ] Display QR code
- [ ] Show compliance info
- [ ] Sustainability dashboard
- [ ] Generate passport PDF

### API Endpoints
```
GET /api/v1/product/{id}/passport
GET /api/v1/product/{id}/passport/qr
GET /api/v1/product/{id}/passport/{version}
POST /api/v1/product/{id}/passport/generate
GET /api/v1/product/{id}/passport/export/pdf
```

### Passport Data Model
```python
{
  "product": {
    "name": string,
    "sku": string,
    "version": string
  },
  "materials": [
    {
      "material_name": string,
      "percentage": number,
      "weight": number,
      "origin": string,
      "recyclability": string
    }
  ],
  "compliance": {
    "rohs": boolean,
    "reach": boolean,
    "ce": string,
    "certifications": [string]
  },
  "sustainability": {
    "carbon_footprint": number,
    "recyclable_percentage": number,
    "recycled_content": number
  },
  "lifecycle": {
    "stage": string,
    "expected_life": string,
    "end_of_life": string,
    "repairability_index": number
  }
}
```

---

## 4. Frontend Tech Stack

### Recommended Setup
- **Framework:** React 18+
- **State Management:** Redux or Zustand
- **Visualization:** D3.js for graphs
- **UI Library:** Material-UI or Tailwind CSS
- **Build Tool:** Vite or Create React App
- **Testing:** Jest + React Testing Library

### New Frontend Components
```
src/
  components/
    GraphVisualization/
      - BOMGraph.jsx
      - GraphControls.jsx
      - NodeDetails.jsx
    ScenarioComparison/
      - BOMComparator.jsx
      - ChangesSummary.jsx
      - ImpactAssessment.jsx
    Passport/
      - PassportViewer.jsx
      - QRCodeDisplay.jsx
      - ComplianceInfo.jsx
      - SustainabilityDashboard.jsx
    Common/
      - Legend.jsx
      - SearchBar.jsx
```

---

## 5. Database Enhancements

### New Tables/Models
```sql
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    product_id INTEGER,
    current_bom_id INTEGER,
    proposed_bom_id INTEGER,
    risk_level VARCHAR(20),
    complexity_score INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (current_bom_id) REFERENCES boms(id),
    FOREIGN KEY (proposed_bom_id) REFERENCES boms(id)
);

CREATE TABLE passports (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    version VARCHAR(20),
    content JSON,
    qr_code_data TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE passport_materials (
    id INTEGER PRIMARY KEY,
    passport_id INTEGER,
    material_name VARCHAR(255),
    percentage FLOAT,
    weight FLOAT,
    origin VARCHAR(255),
    FOREIGN KEY (passport_id) REFERENCES passports(id)
);

CREATE TABLE passport_compliance (
    id INTEGER PRIMARY KEY,
    passport_id INTEGER,
    rohs BOOLEAN,
    reach BOOLEAN,
    certificates TEXT,
    FOREIGN KEY (passport_id) REFERENCES passports(id)
);

CREATE TABLE graph_cache (
    id INTEGER PRIMARY KEY,
    bom_id INTEGER,
    graph_data JSON,
    cached_at TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (bom_id) REFERENCES boms(id)
);
```

---

## 6. Performance Optimization

### Caching Strategy
- Cache graph structures for frequently accessed BOMs
- Cache comparison results for 24 hours
- Use browser caching for visualization libraries

### Graph Algorithm Optimization
- Use BFS/DFS with memoization
- Implement graph pruning for large BOMs
- Use spatial indexing for node positioning

### Frontend Optimization
- Lazy load visualization components
- Virtualize large lists
- Use Web Workers for heavy computation

---

## 7. Testing Strategy

### Backend Tests
```
tests/
  test_visualization/
    - test_graph_builder.py
    - test_scenario_comparator.py
  test_passport/
    - test_passport_generation.py
    - test_qr_code.py
```

### Frontend Tests (React)
```
src/__tests__/
  components/
    - BOMGraph.test.jsx
    - ScenarioComparison.test.jsx
    - PassportViewer.test.jsx
```

### Performance Tests
- Load test graph with 5000+ nodes
- Benchmark comparison algorithm
- Test QR code generation speed

---

## 8. API Response Examples

### Graph Response (D3 format)
```json
{
  "nodes": [
    {"id": "product_SKU001", "label": "Product Name", "type": "product"},
    {"id": "part_P001", "label": "Part P001", "type": "part"}
  ],
  "links": [
    {"source": "product_SKU001", "target": "part_P001", "type": "bom", "quantity": 2}
  ]
}
```

### Scenario Comparison Response
```json
{
  "current_version": "1.0",
  "proposed_version": "2.0",
  "parts_added": 5,
  "parts_removed": 2,
  "parts_modified": 3,
  "change_percentage": 15.5,
  "risk_level": "Medium",
  "complexity_score": 45,
  "recommendations": [
    "Verify design compatibility for all modifications"
  ]
}
```

### Passport Response
```json
{
  "product": {
    "name": "Product Name",
    "sku": "SKU001",
    "version": "1.0"
  },
  "qr_code_url": "/api/v1/product/SKU001/passport/qr",
  "compliance": {
    "rohs": true,
    "reach": true,
    "certifications": ["CE", "UL"]
  },
  "sustainability": {
    "carbon_footprint": 5.2,
    "recyclable_percentage": 95
  }
}
```

---

## 9. Implementation Timeline

### Week 1-2: Graph Visualization
- Implement graph builder backend
- Create D3.js frontend component
- Basic rendering and controls

### Week 2-3: Scenario Comparison
- Implement comparison backend
- Build comparison UI
- Impact assessment display

### Week 3-4: Passport Enhancement
- Add material composition
- Implement compliance metadata
- QR code integration

### Week 4+: Polish & Performance
- Optimization and caching
- Performance testing
- Documentation

---

## 10. Success Metrics (v0.3)

- ✅ Render BOM graphs with 1000+ nodes
- ✅ Scenario comparison completes in < 2 seconds
- ✅ QR code generates in < 500ms
- ✅ Graph interactions are smooth (60 FPS)
- ✅ Passport contains all compliance information
- ✅ 90% test coverage
- ✅ Zero JavaScript errors in production

---

## Next Steps

1. Set up React frontend project
2. Implement D3.js graph visualization
3. Create API endpoints for graph query
4. Build scenario comparison UI
5. Implement passport enhancements
