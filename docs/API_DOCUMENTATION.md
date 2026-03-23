# ThreadPass PLM API Documentation

## Quick Links

- **Interactive API Explorer:** http://localhost:8000/docs (Swagger UI)
- **Alternative Documentation:** http://localhost:8000/redoc (ReDoc)
- **OpenAPI Specification:** http://localhost:8000/api/openapi.json

## Base URL

```
http://localhost:8000/api
```

## Current API Version

All endpoints use `/api/v1/` prefix for future versioning support.

---

## Authentication

**Status:** Not yet implemented (planned for v0.4)

Currently, all endpoints are public. Bearer token authentication will be added in v0.4.

---

## API Endpoints

### Health Check

#### Check Service Health
```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### Dashboard & Metrics

#### Get Overview Metrics
```http
GET /api/overview
```

Get overall PLM metrics and dashboard information.

**Response:**
```json
{
  "total_products": 42,
  "total_changes": 15,
  "affected_products": 8,
  "compliance_coverage": 85.5
}
```

---

### Products

#### List All Products
```http
GET /api/products
```

Retrieve all products in the system.

**Response:**
```json
[
  {
    "id": "prod_001",
    "name": "Industrial Controller",
    "sku": "IC-2024-001",
    "version": "2.1",
    "parts_count": 42
  },
  {
    "id": "prod_002",
    "name": "Smart Sensor",
    "sku": "SS-2024-001",
    "version": "1.3",
    "parts_count": 18
  }
]
```

---

### Digital Passports

#### Generate Product Passport
```http
GET /api/passports/{product_id}
```

Generate a digital product passport for a specific product. The passport contains product information, BOM, compliance data, and sustainability metrics.

**Parameters:**
- `product_id` (required): Product identifier (SKU or ID)

**Response:**
```json
{
  "product": {
    "id": "prod_001",
    "name": "Industrial Controller",
    "sku": "IC-2024-001",
    "version": "2.1"
  },
  "bom": [
    {
      "part_number": "R001",
      "description": "Resistor 10K",
      "category": "Passive",
      "supplier": "Mouser",
      "quantity": 100
    }
  ],
  "compliance": {
    "rohs": true,
    "reach": true,
    "ce_marking": true,
    "certifications": ["CE", "UL"]
  },
  "materials": [
    {
      "material": "Copper",
      "percentage": 15,
      "weight_grams": 45
    }
  ],
  "sustainability": {
    "carbon_footprint": 5.2,
    "recyclable_percentage": 95,
    "recycled_content": 25
  }
}
```

**Errors:**
- `404 Not Found`: Product not found

**Example:**
```bash
curl http://localhost:8000/api/passports/IC-2024-001
```

---

### Engineering Changes

#### List All Changes
```http
GET /api/changes
```

Retrieve all engineering change orders (ECOs) in the system.

**Response:**
```json
[
  {
    "id": "eco_001",
    "eco_number": "ECO-2024-001",
    "title": "Supplier Change for R001",
    "status": "approved",
    "affected_products": ["prod_001", "prod_003"],
    "impact_severity": "medium",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Change Impact Analysis

#### Analyze Change Impact
```http
GET /api/impact/{change_id}
```

Analyze the impact of an engineering change across the product portfolio. Shows which products are affected and the blast radius.

**Parameters:**
- `change_id` (required): Change order identifier

**Response:**
```json
{
  "change": {
    "id": "eco_001",
    "eco_number": "ECO-2024-001",
    "title": "Supplier Change for R001",
    "description": "Changing resistor supplier from Mouser to Digi-Key"
  },
  "affected_products": {
    "direct": ["prod_001", "prod_003"],
    "indirect": ["prod_005"],
    "total": 3
  },
  "impact_analysis": {
    "parts_affected": 2,
    "boms_affected": 3,
    "lead_time_impact": "2 weeks",
    "cost_impact": 15.5
  },
  "impact_severity": "medium",
  "recommendations": [
    "Schedule supplier qualification",
    "Update BOM versions",
    "Notify affected teams"
  ]
}
```

**Errors:**
- `404 Not Found`: Change not found

**Example:**
```bash
curl http://localhost:8000/api/impact/ECO-2024-001
```

---

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong",
  "status": 400
}
```

### Common Error Codes

| Status | Meaning |
|--------|---------|
| 200 | OK - Request succeeded |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal error |

---

## Data Models

### Product

```json
{
  "id": "prod_001",
  "name": "Product Name",
  "sku": "SKU-2024-001",
  "version": "1.0",
  "parts_count": 25,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Part

```json
{
  "part_number": "R001",
  "description": "Resistor 10K",
  "category": "Passive",
  "supplier": "Mouser",
  "quantity": 100,
  "cost": 0.05,
  "lead_time_days": 14,
  "status": "active"
}
```

### Engineering Change Order (ECO)

```json
{
  "id": "eco_001",
  "eco_number": "ECO-2024-001",
  "title": "Change Title",
  "description": "Detailed description",
  "status": "draft|approved|implemented",
  "priority": "low|medium|high|critical",
  "affected_parts": ["R001", "C001"],
  "affected_products": ["prod_001"],
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": "user_123"
}
```

### Compliance Information

```json
{
  "rohs": true,
  "reach": true,
  "ce_marking": true,
  "certifications": ["CE", "UL", "FCC"],
  "last_audit": "2023-12-15T00:00:00Z"
}
```

---

## Rate Limiting

**Status:** Not yet implemented

Rate limiting will be added in a future release.

---

## Pagination

**Status:** Not yet implemented

Pagination support will be added for endpoints returning large datasets. Currently all data is returned.

---

## Filtering & Sorting

Support for filtering and sorting will be added in v0.2:

```http
# Planned in future versions
GET /api/products?status=active&sort=name&limit=10
GET /api/changes?severity=high&status=pending
```

---

## Sample Requests

### Using cURL

```bash
# Get all products
curl http://localhost:8000/api/products

# Get specific passport
curl http://localhost:8000/api/passports/IC-2024-001

# Analyze change impact
curl http://localhost:8000/api/impact/ECO-2024-001
```

### Using Python

```python
import requests

# Get all products
response = requests.get("http://localhost:8000/api/products")
products = response.json()

# Get passport
response = requests.get("http://localhost:8000/api/passports/IC-2024-001")
passport = response.json()

# Analyze change
response = requests.get("http://localhost:8000/api/impact/ECO-2024-001")
impact = response.json()
```

### Using JavaScript

```javascript
// Get all products
fetch("http://localhost:8000/api/products")
  .then(r => r.json())
  .then(data => console.log(data));

// Get passport
fetch("http://localhost:8000/api/passports/IC-2024-001")
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## Upcoming Features (v0.2+)

### Coming in v0.2
- ✅ CSV BOM import endpoint
- ✅ Excel BOM import endpoint
- ✅ Markdown report export
- ✅ Supplier management endpoints
- ✅ Pagination support

### Coming in v0.3
- ✅ Graph visualization endpoint
- ✅ BOM comparison endpoint
- ✅ Scenario analysis endpoints
- ✅ Enhanced passport with QR codes

### Coming in v0.4
- ✅ Authentication & authorization
- ✅ Write endpoints (POST/PUT/DELETE)
- ✅ User management
- ✅ Audit logging

### Coming in v1.0
- ✅ ERP connector endpoints
- ✅ MES integration endpoints
- ✅ Policy engine endpoints
- ✅ Signed digital passports

---

## API Testing

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and click "Execute"

### Using cURL

```bash
curl -X GET "http://localhost:8000/api/products" \
  -H "Content-Type: application/json"
```

### Using Postman

1. Import the OpenAPI spec from http://localhost:8000/api/openapi.json
2. Create requests for each endpoint
3. Test with various parameters

---

## Troubleshooting

### API Not Responding
```bash
# Check service health
curl http://localhost:8000/api/health

# Verify server is running
ps aux | grep uvicorn
```

### 404 Errors
- Verify the endpoint URL is correct
- Check parameters are properly formatted
- Ensure resource ID exists

### JSON Parse Errors
- Ensure Content-Type header is set to `application/json`
- Verify JSON payload is valid

---

## Support & Documentation

- **Development Setup:** See [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Architecture:** See [DEVELOPMENT_PHASES.md](DEVELOPMENT_PHASES.md)
- **Issues:** Report on [GitHub Issues](https://github.com/krishnajbaride/PLMDigitalPassport/issues)

---

## API Changelog

### v0.1.0 (Current)
- Initial API release
- Health check endpoint
- Products listing
- Passport generation
- Change impact analysis
- Overview metrics

### Planned Changes
See [DEVELOPMENT_PHASES.md](DEVELOPMENT_PHASES.md) for upcoming features and breaking changes.
