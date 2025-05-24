#!/usr/bin/env bash
set -e

# 1. Run static code analysis with flake8
flake8 src

# 2. Run tests with pytest
pytest src/tests 
