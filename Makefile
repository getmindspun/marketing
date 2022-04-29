NAME := marketing

all: lint test

flake8:
	flake8 *.py marketing scripts/*.py
.PHONY: flake8

pylint_pkg:
	pylint $(NAME) *.py
.PHONY: pylint_pkg

pylint_scripts:
	pylint scripts/*.py --disable=invalid-name
.PHONY: pylint_scripts

pylint_tests:
	PYTHONPATH=. pylint tests/* --disable=missing-module-docstring,missing-function-docstring,duplicate-code,unused-argument,too-many-arguments
.PHONY: pylint_tests

pylint: pylint_pkg pylint_tests pylint_scripts
.PHONY: pylint

lint: flake8 pylint
.PHONY: lint

test:
	PYTHONPATH=. pytest -xv tests
.PHONY: test

coverage:
	PYTHONPATH=. pytest --cov=$(NAME) --cov-report=term-missing --cov-fail-under=100 tests/
.PHONY: coverage
