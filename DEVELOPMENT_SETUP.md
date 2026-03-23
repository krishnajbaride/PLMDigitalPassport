# ThreadPass PLM - Development Setup Guide

## Prerequisites

### System Requirements
- **OS:** macOS 11+, Ubuntu 20.04+, or Windows 10+ (with WSL2)
- **Python:** 3.10 or higher
- **Node.js:** 16+ (for frontend development in later phases)
- **Git:** 2.30+
- **Docker:** 20.10+ (optional but recommended)

### Required Tools
- Git
- Python virtual environment (`venv`)
- PostgreSQL client utilities (optional)
- curl or Postman (for API testing)

---

## Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/krishnajbaride/PLMDigitalPassport.git
cd PLMDigitalPassport
```

### 2. Create Virtual Environment
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 4. Run Tests
```bash
pytest
```

### 5. Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access the application:**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Detailed Setup

### Step 1: Environment Configuration

Create `.env` file in project root:

```bash
# .env
# Database (SQLite for development)
DATABASE_URL=sqlite:///./threadpass.db

# For PostgreSQL in production
# DATABASE_URL=postgresql://user:password@localhost/threadpass_db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-min-32-characters-long
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24

# API Configuration
API_TITLE=ThreadPass PLM API
API_VERSION=0.1.0
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=INFO
```

Copy from template:
```bash
cp .env.example .env
```

### Step 2: Database Setup

#### SQLite (Development - Default)
```bash
# Database is auto-created on first run
# No additional setup needed
```

#### PostgreSQL (Production/Advanced)
```bash
# Install PostgreSQL
# macOS
brew install postgresql

# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# Windows: Download from https://www.postgresql.org/download/windows/

# Create database and user
createdb threadpass_db
createuser threadpass -P  # It will prompt for password
psql threadpass_db

# In PostgreSQL prompt:
GRANT ALL PRIVILEGES ON DATABASE threadpass_db TO threadpass;
\q
```

Update `.env`:
```
DATABASE_URL=postgresql://threadpass:password@localhost/threadpass_db
```

### Step 3: Run Database Migrations

```bash
# Using Alembic (when available in v0.4)
alembic upgrade head

# For now, SQLite will auto-create schema
python -m app.cli init-db
```

### Step 4: Create Test Data (Optional)

```bash
python -m app.cli seed-db
```

This creates:
- Sample users
- Test BOMs
- Sample parts
- Test ECOs

### Step 5: Run the Application

```bash
# Development mode with hot-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Development Workflow

### Code Structure
```
threadpass-plm/
├── app/
│   ├── main.py              # FastAPI application setup
│   ├── cli.py               # Command-line interface
│   ├── schemas.py           # Pydantic data models
│   ├── services.py          # Business logic
│   ├── repository.py        # Data access layer
│   ├── importers/           # v0.2: Import functionality
│   ├── exporters/           # v0.2: Export functionality
│   ├── visualization/       # v0.3: Graph/visualization
│   ├── auth/                # v0.4: Authentication
│   ├── database/            # v0.4: Database models
│   ├── connectors/          # v1.0: ERP integration
│   └── static/              # Frontend files
├── tests/
│   ├── test_api.py          # API endpoint tests
│   ├── test_services.py     # Business logic tests
│   ├── test_importers.py    # Import tests
│   └── conftest.py          # Pytest fixtures
├── docs/
│   ├── phase-v0.2/
│   ├── phase-v0.3/
│   ├── phase-v0.4/
│   └── phase-v1.0/
├── .github/
│   └── workflows/           # CI/CD workflows
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── pytest.ini              # Pytest configuration
```

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow code style guidelines
   - Write tests for new code
   - Update documentation

3. **Run tests locally:**
   ```bash
   pytest -v
   ```

4. **Check code quality:**
   ```bash
   black app tests
   flake8 app tests
   isort app tests
   ```

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request on GitHub**

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_get_parts

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Test Structure
```python
# tests/test_example.py
import pytest
from app.services import ExampleService

@pytest.fixture
def service():
    """Create service instance for testing"""
    return ExampleService()

def test_example_operation(service):
    """Test example operation"""
    result = service.do_something()
    assert result is not None
```

### Writing Tests

Best practices:
- Use fixtures for common setup
- One assertion per test (ideally)
- Test both happy path and error cases
- Use descriptive test names
- Add docstrings explaining what's tested

---

## API Development

### Creating a New Endpoint

1. **Define the data model (schemas.py):**
```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
```

2. **Implement the service logic (services.py):**
```python
class ItemService:
    def create_item(self, item_data: ItemCreate) -> dict:
        # Business logic here
        return item_data.dict()
```

3. **Create the endpoint (main.py):**
```python
@app.post("/api/v1/items")
async def create_item(item: ItemCreate):
    return await item_service.create_item(item)
```

4. **Add tests (tests/test_api.py):**
```python
def test_create_item(client):
    response = client.post("/api/v1/items", json={"name": "Test"})
    assert response.status_code == 201
```

### API Documentation

Automatically generated at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Add docstrings to automatically document endpoints:
```python
@app.get("/api/v1/items/{id}")
async def get_item(id: int):
    """
    Get a specific item by ID.
    
    - **id**: The item ID
    
    Returns:
        - Item data with all fields
    """
    pass
```

---

## Debugging

### Enable Debug Mode

Set in `.env`:
```
DEBUG=True
```

### Using Python Debugger

```python
# In your code
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

Then in terminal:
```
(Pdb) step       # Step through code
(Pdb) next       # Execute next line
(Pdb) continue   # Continue execution
(Pdb) print var  # Print variable
```

### Using VS Code Debugger

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "purpose": "debug"
    }
  ]
}
```

Then press F5 to debug.

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Docker Development

### Build Docker Image

```bash
docker build -t threadpass-plm:latest .
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Docker Compose Services

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./threadpass.db
    volumes:
      - .:/app
  
  postgres:  # Optional for production
    image: postgres:15
    ports:
      - "5432:5432"
```

---

## Environment Variables

### Development
```bash
DEBUG=True
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Production
```bash
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
```

### All Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///threadpass.db | Database connection string |
| JWT_SECRET_KEY | - | Secret key for JWT (required) |
| JWT_ALGORITHM | HS256 | JWT signing algorithm |
| JWT_ACCESS_TOKEN_EXPIRE_HOURS | 24 | Token expiration hours |
| DEBUG | False | Enable debug mode |
| LOG_LEVEL | INFO | Logging level |
| API_TITLE | ThreadPass PLM API | API title |
| API_VERSION | 0.1.0 | API version |
| CORS_ORIGINS | - | Comma-separated CORS origins |

---

## Common Commands

```bash
# Create new branch
git checkout -b feature/name

# Pull latest changes
git pull origin master

# View uncommitted changes
git diff

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Clean up merged branches
git branch -d branch-name
```

---

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>
```

### Database Locked
```bash
# Remove SQLite lock files
rm threadpass.db-wal
rm threadpass.db-shm

# Restart application
```

### Dependencies Conflict
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall clean
pip install -r requirements.txt --force-reinstall
```

---

## Getting Help

1. **Check documentation:** Review docs/ folder
2. **Search issues:** GitHub Issues
3. **Ask in discussions:** GitHub Discussions
4. **Join Slack:** (if available)
5. **Create issue:** If bug or feature request

---

## Next Steps

1. ✅ Complete **Development Setup Guide** (you are here)
2. ⬜ Run `pytest` to verify setup
3. ⬜ Make your first code change
4. ⬜ Create a pull request
5. ⬜ Review CI/CD pipeline results
