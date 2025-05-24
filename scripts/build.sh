#!/usr/bin/env bash
set -e

# 1. Run ruff to check and fix linting errors
ruff check --fix src

# 2. Run ruff formatter
ruff format src

# 3. Run tests with pytest
pytest src/tests 
