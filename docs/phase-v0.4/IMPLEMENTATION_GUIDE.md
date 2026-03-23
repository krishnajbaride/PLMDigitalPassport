"""
Phase v0.4 - Implementation Guide
Persistence Layer, Authentication, and Write APIs
"""

# Phase v0.4 Implementation Checklist

## 1. Database Setup

### Database Selection
- **Development:** SQLite (zero-config, lightweight)
- **Production:** PostgreSQL (scalable, robust)
- **ORM:** SQLAlchemy 2.0

### Migration Strategy
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Core Schema Design

```python
# Users and Authentication
class User(Base):
    user_id: int
    username: str (unique)
    email: str (unique)
    password_hash: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: datetime

class Role(Base):
    role_id: int
    name: str (unique)
    description: str
    permissions: List[str]

class AuditLog(Base):
    log_id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: int
    changes: JSON
    timestamp: datetime
    ip_address: str

# Product Data
class Product(Base):
    product_id: int
    sku: str (unique)
    name: str
    description: str
    version: str
    created_by: int
    created_at: datetime
    updated_at: datetime

class Part(Base):
    part_id: int
    part_number: str (unique)
    description: str
    category: str
    supplier_id: int
    cost: float
    lead_time_days: int
    created_at: datetime

class BOM(Base):
    bom_id: int
    product_id: int
    version: str
    created_by: int
    created_at: datetime
    is_active: bool

class BOMLEntry(Base):
    entry_id: int
    bom_id: int
    part_id: int
    quantity: int
    sequence: int

class Supplier(Base):
    supplier_id: int
    name: str
    contact: str
    email: str
    country: str
    quality_rating: float

class ECO(Base):
    eco_id: int
    eco_number: str (unique)
    title: str
    description: str
    status: str  # draft, approved, rejected, implemented
    priority: str
    created_by: int
    created_at: datetime
    approved_by: int
    approved_at: datetime
    impact_analysis: JSON

# Change Tracking
class ChangeLog(Base):
    change_id: int
    parent_id: int  # BOM, Part, ECO ID
    entity_type: str
    operation: str  # insert, update, delete
    before_value: JSON
    after_value: JSON
    changed_by: int
    changed_at: datetime
```

---

## 2. Authentication Implementation

### Setup
- [x] JWT handler (`app/auth/jwt_handler.py`)
- [ ] Password hashing (bcrypt)
- [ ] Token refresh mechanism
- [ ] Session management
- [ ] Email verification (optional)

### JWT Configuration
```python
# app/config.py
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "your-secret-key-min-32-chars"
JWT_ACCESS_TOKEN_EXPIRE_HOURS = 24
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 30
```

### API Endpoints
```
POST /api/v1/auth/login - Login user
POST /api/v1/auth/register - Register new user
POST /api/v1/auth/refresh - Refresh access token
POST /api/v1/auth/logout - Logout user
GET /api/v1/auth/me - Get current user info
POST /api/v1/auth/change-password - Change password
```

### Login Request/Response
```json
// Request
{
  "username": "jdoe",
  "password": "securepassword"
}

// Response (200 OK)
{
  "access_token": "eyJ0eXAiOiJKV1QiL...",
  "refresh_token": "eyJ0eXAiOiJKV1QiL...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "username": "jdoe",
    "email": "jdoe@example.com",
    "roles": ["engineer"]
  }
}
```

---

## 3. Authorization & RBAC

### Implementation
- [x] RBAC manager (`app/auth/jwt_handler.py`)
- [ ] Middleware for permission checks
- [ ] Decorator for route protection
- [ ] Fine-grained permissions
- [ ] Audit logging for all access

### Role Definitions
```
ADMIN
  - Create/Read/Update/Delete all
  - Manage users & roles
  - View audit logs
  - Approve ECOs

ENGINEER
  - Create/Update parts & BOMs
  - Create/Update ECOs
  - View analysis
  - Import BOMs
  - Export reports

VIEWER
  - Read-only access
  - View analysis
  - Export reports

SUPPLIER
  - View own parts
  - Access limited info
```

### Permission Middleware Example
```python
from fastapi import Depends, HTTPException

async def require_permission(permission: Permission):
    async def check(current_user: dict = Depends(get_current_user)):
        rbac.check_permission(current_user["roles"], permission)
        return current_user
    return check

@app.post("/api/v1/parts")
async def create_part(
    part_data: dict,
    current_user: dict = Depends(require_permission(Permission.CREATE_PART))
):
    # Audit log
    audit_service.log(current_user["user_id"], "create_part", part_data)
    return await part_service.create(part_data)
```

---

## 4. Write APIs Implementation

### Part Management
```
POST /api/v1/parts - Create part
PUT /api/v1/parts/{id} - Update part
DELETE /api/v1/parts/{id} - Delete part
GET /api/v1/parts - List parts
GET /api/v1/parts/{id} - Get part
POST /api/v1/parts/{id}/suppliers - Add supplier
```

### BOM Management
```
POST /api/v1/boms - Create BOM
PUT /api/v1/boms/{id} - Update BOM
DELETE /api/v1/boms/{id} - Delete BOM
POST /api/v1/boms/{id}/entries - Add BOM entry
PUT /api/v1/boms/{id}/entries/{entry_id} - Update entry
DELETE /api/v1/boms/{id}/entries/{entry_id} - Remove entry
POST /api/v1/boms/{id}/release - Release BOM version
```

### ECO Management
```
POST /api/v1/ecos - Create ECO
PUT /api/v1/ecos/{id} - Update ECO
DELETE /api/v1/ecos/{id} - Delete ECO
POST /api/v1/ecos/{id}/approve - Approve ECO
POST /api/v1/ecos/{id}/reject - Reject ECO
POST /api/v1/ecos/{id}/implement - Mark as implemented
GET /api/v1/ecos/{id}/impact-analysis - Get impact analysis
```

### Request/Response Examples
```json
// Create Part Request
{
  "part_number": "R001",
  "description": "Resistor 10K",
  "category": "Passive",
  "supplier_id": 1,
  "cost": 0.05,
  "lead_time_days": 14,
  "alternates": ["R001-ALT", "R001-ALT2"]
}

// Create BOM Request
{
  "product_id": 1,
  "version": "2.0",
  "entries": [
    {
      "part_id": 1,
      "quantity": 100,
      "sequence": 1
    },
    {
      "part_id": 2,
      "quantity": 50,
      "sequence": 2
    }
  ]
}

// Create ECO Request
{
  "eco_number": "ECO-2024-001",
  "title": "Supplier change for R001",
  "description": "Changing supplier from Mouser to Digi-Key",
  "priority": "medium",
  "affected_parts": [1],
  "affected_products": [1, 2],
  "proposed_changes": {...}
}
```

---

## 5. Audit Logging

### Implementation
- [ ] AuditService for logging all changes
- [ ] Middleware for automatic logging
- [ ] Audit API endpoints
- [ ] Compliance reports

### Audit Logging Strategy
```python
class AuditService:
    def log(self, user_id: int, action: str, 
            resource_type: str, resource_id: int,
            before: dict = None, after: dict = None):
        """Log action for audit trail"""
        
    def get_audit_trail(self, resource_type: str, 
                        resource_id: int) -> List[dict]:
        """Get complete audit history for resource"""

# Middleware
@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    # Log the request/response
    return response
```

### Audit API Endpoints
```
GET /api/v1/audit/trail/{resource_type}/{resource_id}
GET /api/v1/audit/user/{user_id}
GET /api/v1/audit/report - Generate audit report
```

---

## 6. Database Migrations

### Using Alembic
```bash
# Generate migration
alembic revision --autogenerate -m "Add suppliers table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current version
alembic current
```

### Migration Files Structure
```
alembic/
  versions/
    001_initial_schema.py
    002_add_audit_log.py
    003_add_suppliers.py
```

---

## 7. Error Handling

### Standard Error Responses
```json
{
  "error": {
    "code": "PART_NOT_FOUND",
    "message": "Part with ID 123 not found",
    "status": 404,
    "timestamp": "2024-03-22T10:30:00Z"
  }
}
```

### Exception Classes
```python
class ThreadPassException(Exception):
    pass

class PartNotFound(ThreadPassException):
    status_code = 404

class UnauthorizedException(ThreadPassException):
    status_code = 401

class PermissionDeniedException(ThreadPassException):
    status_code = 403

class ValidationException(ThreadPassException):
    status_code = 400
```

---

## 8. Database Performance

### Indexes
```sql
CREATE INDEX idx_part_number ON parts(part_number);
CREATE INDEX idx_product_sku ON products(sku);
CREATE INDEX idx_eco_status ON ecos(status);
CREATE INDEX idx_audit_user_date ON audit_logs(user_id, changed_at DESC);
CREATE INDEX idx_bom_product ON boms(product_id);
```

### Query Optimization
- Use lazy loading for relationships
- Implement pagination (limit 100, default 10)
- Cache frequently accessed data
- Use connection pooling

---

## 9. Backup & Recovery

### PostgreSQL Backup Strategy
```bash
# Full backup
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql

# Automated daily backups
0 2 * * * pg_dump dbname | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz
```

---

## 10. Testing Strategy

### Database Tests
```python
# tests/test_database.py
@pytest.fixture
def test_db():
    # Create test database
    # Run migrations
    yield db
    # Clean up

def test_create_part(test_db):
    # Test part creation
    pass

def test_constraints(test_db):
    # Test unique constraints
    # Test foreign keys
    pass
```

### API Tests
```python
# tests/test_api.py
def test_create_part_auth(client):
    # Test requires authentication
    response = client.post("/api/v1/parts", json={...})
    assert response.status_code == 401

def test_create_part_permission(client, authorized_user):
    # Test requires permission
    pass
```

---

## 11. Deployment Configuration

### Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost/threadpass_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,https://example.com
```

### Docker Compose Setup
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: threadpass_db
      POSTGRES_USER: threadpass
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    environment:
      DATABASE_URL: postgresql://threadpass:secure_password@postgres/threadpass_db
    depends_on:
      - postgres
    ports:
      - "8000:8000"

volumes:
  postgres_data:
```

---

## 12. Implementation Timeline

### Week 1-2: Database & ORM
- Set up SQLAlchemy
- Create migration framework
- Design and implement schema

### Week 2-3: Authentication
- Implement JWT handling
- Create login/register endpoints
- Database schema for users

### Week 3-4: Authorization & RBAC
- Implement permission system
- Create middleware
- Add audit logging

### Week 4-5: Write APIs
- Implement part CRUD
- Implement BOM management
- Implement ECO management

### Week 5+: Polish & Testing
- Comprehensive testing
- Performance optimization
- Documentation

---

## 13. Success Metrics (v0.4)

- ✅ 99.9% database uptime
- ✅ Authentication latency < 100ms
- ✅ All queries complete in < 1s
- ✅ 95% test coverage for APIs
- ✅ Zero data loss
- ✅ Complete audit trail
- ✅ RBAC working for all endpoints
