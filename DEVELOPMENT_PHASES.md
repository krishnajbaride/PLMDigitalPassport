# ThreadPass PLM - Development Phases

## Project Overview
ThreadPass PLM is a composable PLM microservice that turns BOM and ECO data into digital product passports and graph-style change-impact reports.

---

## Phase v0.1 - MVP (Current Baseline)
**Status:** ✅ Complete - Foundation

### Features
- FastAPI backend with REST API
- Sample BOM and ECO (Engineering Change Order) data
- Digital product passport JSON generation
- Engineering change blast-radius analysis
- FastAPI interactive documentation (/docs)
- CLI for basic operations
- Docker containerization
- GitHub Actions CI/CD
- Unit tests with pytest

### Deliverables
- Core API endpoints for BOM and ECO analysis
- Basic change impact analysis
- Passport generation in JSON format
- CLI interface
- Docker setup
- CI/CD pipeline

### Key Files
- `app/main.py` - FastAPI application
- `app/services.py` - Business logic
- `app/schemas.py` - Data models
- `app/cli.py` - Command-line interface
- `data/` - Sample data files

---

## Phase v0.2 - Import/Export & Enhanced Data
**Priority:** HIGH | **Timeline:** 4-6 weeks

### Features
- ✅ CSV BOM import functionality
- ✅ Excel BOM import functionality
- ✅ Export impact analysis as Markdown report
- ✅ Add realistic supplier fields
- ✅ Support for alternate components
- ✅ Validation and error handling for imports
- ✅ Sample import templates

### Tasks
1. Create CSV/Excel parser module
   - `app/importers/csv_importer.py`
   - `app/importers/excel_importer.py`
2. Extend schema to support supplier data
   - Update `app/schemas.py` with supplier models
3. Create Markdown export module
   - `app/exporters/markdown_exporter.py`
4. Build import/export endpoints
5. Add integration tests
6. Create user guide for imports

### Database Schema Changes
- Add supplier table and relationships
- Support for alternate parts
- Import history tracking

### API Endpoints
- `POST /api/v1/import/csv` - Import CSV BOM
- `POST /api/v1/import/excel` - Import Excel BOM
- `GET /api/v1/analysis/{id}/export/markdown` - Export as Markdown
- `GET /api/v1/suppliers` - List suppliers
- `POST /api/v1/suppliers` - Add supplier

---

## Phase v0.3 - Visualization & Scenario Analysis
**Priority:** HIGH | **Timeline:** 6-8 weeks

### Features
- ✅ Interactive graph visualization of product structure
- ✅ Scenario comparison tool (current vs proposed BOM)
- ✅ Richer digital passport profile
- ✅ QR code generation for passport
- ✅ Visual change impact display
- ✅ Component dependency graphs

### Tasks
1. Create graph visualization engine
   - `app/visualization/graph_builder.py`
   - `app/visualization/d3_renderer.py`
2. Build scenario comparison engine
   - `app/services/scenario_service.py`
3. Enhance passport generation
   - `app/services/passport_service.py`
4. Add QR code generation
   - `app/utilities/qr_generator.py`
5. Frontend enhancements
   - Update `app/static/app.js`
   - Update `app/static/index.html`
   - Add D3.js for graph visualization

### Frontend Components
- Graph visualization canvas
- Scenario comparison UI
- Interactive passport viewer
- QR code display

### API Endpoints
- `GET /api/v1/bom/{id}/graph` - Get graph representation
- `POST /api/v1/scenario/compare` - Compare BOMs
- `GET /api/v1/passport/{id}/qr` - Get QR code

---

## Phase v0.4 - Persistence & Authentication
**Priority:** MEDIUM | **Timeline:** 6-8 weeks

### Features
- ✅ SQLite or PostgreSQL persistence layer
- ✅ User authentication & authorization
- ✅ Role-based access control (RBAC)
- ✅ Write APIs for part creation
- ✅ Write APIs for BOM management
- ✅ Write APIs for change orders
- ✅ User session management
- ✅ Audit logging

### Tasks
1. Set up database layer
   - `app/database/models.py` - SQLAlchemy ORM models
   - `app/database/connection.py` - DB connection management
   - Create migration scripts (Alembic)
2. Implement authentication
   - `app/auth/jwt_handler.py` - JWT token management
   - `app/auth/security.py` - Password hashing, validation
   - OAuth2 optional integration
3. Add authorization
   - `app/auth/permissions.py` - RBAC logic
   - Middleware for permission checks
4. Create write endpoints
   - `POST /api/v1/parts` - Create part
   - `PUT /api/v1/parts/{id}` - Update part
   - `DELETE /api/v1/parts/{id}` - Delete part
   - `POST /api/v1/boms` - Create BOM
   - `POST /api/v1/changes` - Create ECO
5. Add audit logging
   - `app/services/audit_service.py`
6. Create user management endpoints
   - User CRUD operations
   - Role assignment

### Database Models
- Users
- Roles
- Permissions
- Parts
- BOMs
- ECOs
- Audit logs

### Security Features
- JWT authentication
- Password encryption (bcrypt)
- Session management
- Rate limiting
- CORS configuration
- Audit trail

---

## Phase v1.0 - Enterprise Features
**Priority:** MEDIUM | **Timeline:** 8-12 weeks

### Features
- ✅ Pluggable connectors to ERP systems
- ✅ MES (Manufacturing Execution System) integration
- ✅ Document system connectors
- ✅ Signed digital product passports (PKI)
- ✅ Policy engine for compliance rules
- ✅ Lifecycle state management
- ✅ Advanced compliance reporting
- ✅ Multi-tenant support

### Tasks
1. Create connector framework
   - `app/connectors/base_connector.py` - Abstract connector
   - `app/connectors/erp/` - ERP implementations (SAP, Oracle, NetSuite)
   - `app/connectors/mes/` - MES implementations
   - `app/connectors/document/` - Document system connectors
2. Implement certificate/PKI handling
   - `app/security/certificate_handler.py`
   - `app/security/passport_signer.py`
3. Build policy engine
   - `app/policy/engine.py`
   - `app/policy/rules.py`
   - `app/policy/evaluator.py`
4. Add compliance reporting
   - `app/reporting/compliance_reporter.py`
   - `app/reporting/lifecycle_reporter.py`
5. Implement multi-tenancy
   - `app/tenancy/tenant_manager.py`
   - Tenant isolation at DB level
6. Create webhooks and event system
   - `app/events/event_bus.py`
   - `app/webhooks/manager.py`

### Connectors to Implement
- ERP: SAP, Oracle, NetSuite, Odoo
- MES: MES-IX compliant systems
- Document: Sharepoint, Confluence, AWS S3
- Identity: LDAP, OAuth2, SAML

### Compliance Features
- Digital Product Passport (DPP) support per EU ESPR
- Material composition tracking
- Sustainability metrics
- Lifecycle compliance rules
- SBoM (Software Bill of Materials) tracking

### Advanced Features
- Webhook notifications
- Event streaming (Kafka/RabbitMQ ready)
- Advanced search and filtering
- Custom reporting engine
- Batch processing for large operations

---

## Implementation Strategy

### Phase Workflow
1. **v0.2**: Focus on data flexibility (CSV/Excel, Markdown export)
2. **v0.3**: Enhance UX with visualization and scenario planning
3. **v0.4**: Add enterprise-grade persistence and security
4. **v1.0**: Open ecosystem with connectors and compliance

### Development Best Practices
- Test-driven development (TDD)
- API versioning (v1, v2, etc.)
- Backward compatibility
- Comprehensive logging
- Docker containerization for each phase
- Documentation for each phase
- Release notes and changelog

### Quality Assurance
- Unit tests (minimum 80% coverage)
- Integration tests
- API contract testing
- Load testing
- Security testing (OWASP Top 10)
- Accessibility testing

### Deployment
- Docker Compose for local development
- Kubernetes manifests for v0.4+
- GitHub Actions CI/CD
- Rollback strategy
- Database migration strategy

---

## Team & Skills Required

### Phase v0.2
- Backend Developer (Python/FastAPI)
- Data Security Specialist (validation)
- Tech Writer

### Phase v0.3
- Backend Developer
- Frontend Developer (React/Vue.js)
- UX/UI Designer
- Data Visualization Specialist

### Phase v0.4
- Backend Developer (Database specialist)
- Security Engineer
- DevOps Engineer
- QA Engineer

### Phase v1.0
- Senior Backend Architect
- Integration Specialist
- Security/Compliance Specialist
- Solutions Architect

---

## Success Metrics

### v0.2
- CSV/Excel import success rate > 95%
- Markdown export fully automated
- Supplier data validation complete

### v0.3
- Graph renders for BOMs with 1000+ components
- Scenario comparison < 2s response time
- Accessibility score > 90

### v0.4
- 99.9% uptime
- Authentication latency < 100ms
- Audit log completeness 100%
- RBAC test coverage > 90%

### v1.0
- Connector framework supports 5+ ERP systems
- Passport signature verification 100% success
- Policy engine evaluation time < 500ms
- DPP compliance certification achieved

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| ERP connector complexity | HIGH | Modular design, vendor partnerships |
| Performance at scale | HIGH | Load testing in v0.3, caching strategy |
| Regulatory changes | MEDIUM | Policy engine flexibility, monitoring |
| Security breaches | HIGH | Penetration testing, bug bounty program |
| Team skill gaps | MEDIUM | Knowledge sharing, training, documentation |

---

## Next Steps

1. **Immediate (v0.2)**
   - Create `/app/importers/` directory
   - Design CSV/Excel schema
   - Build import validation layer
   - Create markdown exporter

2. **Short-term (v0.3)**
   - Plan frontend tech stack (React recommended)
   - Design graph data structures
   - Create visualization specifications

3. **Medium-term (v0.4)**
   - Evaluate database (SQLite for MVP, PostgreSQL for production)
   - Design auth architecture
   - Create security policies

4. **Long-term (v1.0)**
   - Research connector patterns
   - Evaluate PKI/certificate solutions
   - Plan policy engine DSL
