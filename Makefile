SHELL := /bin/bash

.PHONY: setup lint test

setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && pip install -e ".[dev]"

lint:
	. .venv/bin/activate && python -m compileall -q src tests
	. .venv/bin/activate && ruff check src tests

test:
	. .venv/bin/activate && python -m unittest discover -s tests -p "test_*.py" -q
