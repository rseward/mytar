.PHONY: venv deps test lint clean install

# Python interpreter
UV := uv

# Directories
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# Test files
TEST_FILES := tests/

help: Makefile
	@echo "Available targets:"
	@echo "  make venv    - Initialize the virtual environment using uv"
	@echo "  make deps    - Install project dependencies"
	@echo "  make test    - Run project tests"
	@echo "  make lint    - Run ruff lint checks"
	@echo "  make clean   - Remove build artifacts and cache files"
	@echo "  make install - Install the package in editable mode"

venv:
	@echo "Creating virtual environment..."
	@$(UV) venv $(VENV_DIR)
	@echo "Virtual environment created. Activate with: source $(VENV_DIR)/bin/activate"

deps:
	@echo "Installing dependencies..."
	@$(UV) sync --all-extras

test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest $(TEST_FILES) -v

lint:
	@echo "Running ruff lint checks..."
	@$(PYTHON) -m ruff check src/

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache/
	@rm -rf .ruff_cache/
	@rm -rf __pycache__/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

install:
	@echo "Installing package in editable mode..."
	@$(UV) pip install -e .
