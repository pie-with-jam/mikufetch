# Makefile for Mikufetch 🐱‍💻

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Sphinx
SPHINXBUILD := $(PYTHON) -m sphinx
DOCS_SRC := docs
DOCS_BUILD := docs/_build

# Pytest
PYTEST := $(PYTHON) -m pytest

# Package
PACKAGE := mikufetch

.PHONY: help clean install test docs run

help:
	@echo "Available commands:"
	@echo "  make install    - Install Mikufetch locally"
	@echo "  make test       - Run tests with pytest"
	@echo "  make docs       - Build HTML docs with Sphinx"
	@echo "  make clean      - Clean build artifacts and cache"
	@echo "  make run        - Run Mikufetch locally"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e .

test:
	%PYTHON% -m pip install --user pytest || true
	%PYTHON% -m pytest tests/

docs:
	%PYTHON% -m pip install sphinx
	%PYTHON% -m pip install sphinx_rtd_theme
	$(SPHINXBUILD) -b html $(DOCS_SRC) $(DOCS_BUILD)

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf $(DOCS_BUILD)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

run:
	$(PYTHON) -m $(PACKAGE)
