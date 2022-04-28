all: lint

flake8:
	flake8 *.py marketing scripts/*.py
.PHONY: flake8

pylint_scripts:
	pylint scripts/*.py --disable=invalid-name
.PHONY: pylint_scripts

pylint: pylint_scripts
	pylint *.py marketing
.PHONY: pylint

lint: flake8 pylint
.PHONY: lint
