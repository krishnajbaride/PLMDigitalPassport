"""
Phase v0.2 - Implementation Guide
CSV/Excel Import, Markdown Export, and Supplier Management
"""

# Phase v0.2 Implementation Checklist

## 1. CSV/Excel Import Feature

### Backend Implementation
- [x] Create `app/importers/bom_importer.py` - Base importer classes
- [ ] Implement CSV parser with validation
- [ ] Implement Excel parser with validation
- [ ] Add cell reference tracking for error reporting
- [ ] Create import history tracking
- [ ] Add duplicate detection logic
- [ ] Create batch import API endpoint

### Frontend Implementation
- [ ] Create import UI component
- [ ] Add file drag-and-drop support
- [ ] Show import progress indicator
- [ ] Display validation error messages
- [ ] Preview uploaded data before confirmation
- [ ] Show import results summary

### Testing
- [ ] Unit tests for CSV parser
- [ ] Unit tests for Excel parser
- [ ] Integration tests for import endpoints
- [ ] Test with malformed files
- [ ] Test with large files (1000+ rows)
- [ ] Test duplicate handling

### API Endpoints
```
POST /api/v1/import/csv
POST /api/v1/import/excel
GET /api/v1/imports/history
GET /api/v1/imports/{id}/details
```

---

## 2. Markdown Export Feature

### Backend Implementation
- [x] Create `app/exporters/markdown_exporter.py` - Markdown generation
- [ ] Implement impact analysis export format
- [ ] Implement supplier impact export format
- [ ] Implement BOM comparison export format
- [ ] Add customizable report templates
- [ ] Create PDF export (via Markdown conversion)
- [ ] Add HTML export option

### Frontend Implementation
- [ ] Add export button to analysis results
- [ ] Create export format selector
- [ ] Add report generation options (template selection)
- [ ] Implement download functionality
- [ ] Show export progress

### Testing
- [ ] Verify Markdown formatting correctness
- [ ] Test with complex impact scenarios
- [ ] Validate table generation
- [ ] Test special characters in data
- [ ] Verify file sizing and performance

### API Endpoints
```
GET /api/v1/analysis/{id}/export/markdown
POST /api/v1/reports/generate
GET /api/v1/reports/{id}/download
```

---

## 3. Supplier Management

### Backend Implementation
- [ ] Extend Part schema with supplier information
- [ ] Create Supplier model/schema
- [ ] Create supplier CRUD endpoints
- [ ] Implement alternate supplier support
- [ ] Add lead time tracking
- [ ] Add supplier risk scoring
- [ ] Create supplier search/filter

### Database Schema
```python
class Supplier(Base):
    id: int
    name: str
    contact: str
    email: str
    phone: str
    country: str
    lead_time_days: int
    quality_rating: float
    cost_rating: float
    sustainability_rating: float
    is_preferred: bool

class PartSupplier(Base):
    part_id: int
    supplier_id: int
    supplier_part_number: str
    unit_cost: float
    minimum_order: int
    preferred: bool
    lead_time_days: int
```

### Frontend Implementation
- [ ] Create supplier management UI
- [ ] Build supplier search/filter interface
- [ ] Add supplier rating visualization
- [ ] Create supplier comparison view

### Testing
- [ ] Test supplier CRUD operations
- [ ] Test alternate supplier selection
- [ ] Test supplier filtering

### API Endpoints
```
GET /api/v1/suppliers
POST /api/v1/suppliers
PUT /api/v1/suppliers/{id}
DELETE /api/v1/suppliers/{id}
GET /api/v1/parts/{id}/suppliers
POST /api/v1/parts/{id}/suppliers
```

---

## 4. CSV Import Template

### Create Sample CSV Templates
- `templates/bom_import_basic.csv` - Basic BOM template
- `templates/bom_import_advanced.csv` - Advanced with suppliers
- `templates/supplier_data_import.csv` - Supplier master data

### Example CSV Format
```
part_number,description,quantity,supplier,model,category,lead_time_weeks,cost,alternates
R001,Resistor 10K,100,Mouser,RES-10K-0603,Passive,2,0.05,
R002,Resistor 1K,50,Digi-Key,RES-1K-0603,Passive,2,0.04,R002-ALT
C001,Capacitor 100nF,200,Newark,CAP-100N-0603,Passive,3,0.08,
IC001,Microcontroller ARM,10,Arrow,MCU-STM32,ICs,4,2.50,IC001-ALT;IC001-ALT2
```

---

## 5. Implementation Priority

### Week 1-2: CSV Import
- Basic CSV parser
- Validation logic
- Error handling
- Simple test cases

### Week 2-3: Excel Import
- Excel parser integration
- Enhanced validation
- File format detection

### Week 3-4: Markdown Export
- Impact analysis export
- Report formatting
- Download functionality

### Week 4-5: Supplier Management
- Schema extensions
- CRUD endpoints
- Supplier search

### Week 5+: Polish
- Performance optimization
- Batch operations
- Advanced features

---

## 6. Dependencies to Add

```
openpyxl>=3.0.0  # Excel support
pandas>=1.3.0    # Advanced CSV/Excel handling
jinja2>=3.0.0    # Report templating
markdown2>=2.4.0 # Enhanced markdown generation
```

Or add to `requirements.txt`:
```
openpyxl==3.8.0
pandas==1.3.0
jinja2==3.0.0
```

---

## 7. Database Migration (if using SQLite/PostgreSQL)

```sql
-- Create Supplier table
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    email VARCHAR(255),
    country VARCHAR(100),
    lead_time_days INTEGER,
    quality_rating FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create PartSupplier relationship
CREATE TABLE part_suppliers (
    id INTEGER PRIMARY KEY,
    part_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    supplier_part_number VARCHAR(255),
    unit_cost FLOAT,
    preferred BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (part_id) REFERENCES parts(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- Create Import History table
CREATE TABLE import_history (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255),
    file_type VARCHAR(10),
    total_rows INTEGER,
    successful_rows INTEGER,
    failed_rows INTEGER,
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER
);
```

---

## 8. Error Handling

### Import Errors to Catch
- [ ] Missing required columns
- [ ] Invalid data types
- [ ] Duplicate part numbers
- [ ] Invalid supplier references
- [ ] Encoding issues
- [ ] File corruption

### Error Response Format
```json
{
  "success": false,
  "error": "CSV format validation failed",
  "validation_errors": [
    "Missing required column: part_number",
    "Row 5: Invalid quantity value 'abc'"
  ],
  "summary": {
    "total_rows": 10,
    "failed_rows": 2,
    "success_rows": 8
  }
}
```

---

## 9. Performance Considerations

- Implement batch processing for large imports (>5000 rows)
- Use pagination for import history
- Cache supplier data
- Index on part_number and supplier

---

## 10. Success Metrics (v0.2)

- ✅ Import CSV files with 1000+ rows
- ✅ Import Excel files with 500+ rows
- ✅ Export impact analysis in < 2 seconds
- ✅ Support for 10+ suppliers per part
- ✅ 95% import success rate
- ✅ Zero data loss in valid imports
- ✅ Comprehensive error reporting
