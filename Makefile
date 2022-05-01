NAME := marketing
REPO := registry.digitalocean.com/mindspun/$(NAME)

BRANCH = $(shell git symbolic-ref --short -q HEAD)
SHA = $(shell git rev-parse --short HEAD)
VERSION = $(BRANCH)-$(SHA)

all: lint test

flake8:
	flake8 *.py marketing scripts/*.py
.PHONY: flake8

pylint_pkg:
	pylint $(NAME) *.py
.PHONY: pylint_pkg

pylint_scripts:
	pylint scripts/*.py --disable=invalid-name,duplicate-code
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

freeze:
	pyenv/bin/pip3 freeze | egrep -v "egg\=$(NAME)|pkg-resources" > requirements.txt
.PHONY: freeze

build:
	docker-compose build $(NAME)
	docker tag $(NAME) $(REPO):$(VERSION)
	@echo Tagged $(VERSION)
.PHONY: docker-build

push:
	docker push $(REPO):$(VERSION)
.PHONY: push

deploy: build push
	scp production.yaml api:/var/mindspun/docker-compose.marketing.yaml
	ssh api /snap/bin/doctl registry login
	ssh api docker pull --quiet $(REPO):$(VERSION)
	# ssh api docker tag $(REPO):latest $(REPO):rollback
	ssh api docker tag $(REPO):$(VERSION) $(REPO):latest
	ssh api docker-compose -f /var/mindspun/docker-compose.marketing.yaml up -d
.PHONY: website

deploy-root:
	scp -r devops/root/* api:/
.PHONY: deploy-root
