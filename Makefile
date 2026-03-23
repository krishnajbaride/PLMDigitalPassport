.PHONY: help install dev test test-cov lint format clean migrate run docker-build docker-up docker-down

.DEFAULT_GOAL := help

# Variables
PYTHON := python
PIP := pip
VENV := .venv
APP := app
TESTS := tests

help:
	@echo "ThreadPass PLM - Development Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run           - Run development server"
	@echo "  make dev           - Run server with auto-reload"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make test-watch    - Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run all linters"
	@echo "  make format        - Format code with black & isort"
	@echo "  make type-check    - Run type checking with mypy"
	@echo ""
	@echo "Database:"
	@echo "  make migrate       - Run database migrations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make clean-all     - Clean everything including venv"
	@echo ""

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

run:
	uvicorn $(APP).main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn $(APP).main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest $(TESTS)/ -v

test-cov:
	pytest $(TESTS)/ --cov=$(APP) --cov-report=html --cov-report=term-missing -v
	@echo "\nCoverage report generated in htmlcov/index.html"

test-watch:
	pytest-watch $(TESTS)/ -v

lint:
	@echo "Running flake8..."
	flake8 $(APP) $(TESTS)
	@echo "Running black check..."
	black --check $(APP) $(TESTS)
	@echo "Running isort check..."
	isort --check-only $(APP) $(TESTS)

format:
	@echo "Formatting with black..."
	black $(APP) $(TESTS)
	@echo "Sorting imports with isort..."
	isort $(APP) $(TESTS)

type-check:
	mypy $(APP) --ignore-missing-imports

migrate:
	@echo "Running database migrations..."
	alembic upgrade head

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -f .coverage

clean-all: clean
	rm -rf $(VENV)/

docker-build:
	docker build -t threadpass-plm:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Git helpers
.PHONY: branch-create branch-delete branch-list push pull

branch-create:
	@read -p "Enter branch name: " branch_name; \
	git checkout -b feature/$$branch_name

branch-delete:
	@read -p "Enter branch name to delete: " branch_name; \
	git branch -D $$branch_name

branch-list:
	git branch -a

push:
	@read -p "Enter branch name to push: " branch_name; \
	git push origin $$branch_name

pull:
	git pull origin main
