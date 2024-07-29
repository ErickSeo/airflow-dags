.PHONY: help mypy isort, lint-check, lint, neat, test, prepare-environment

# Will include both `.env` if it exists (-)
-include .env
export

SHELL := /bin/bash

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

prepare-requirements:
	@echo "Installing project's python requirements..."
	python -m pip install -r requirements/requirements-setup.txt
	python -m pip install -r requirements/requirements-dev.txt
	python -m pip install -r requirements/requirements-test.txt

prepare-environment: prepare-requirements
	echo "Project's environment is ready!!"

prepare-venvironment:
	
	@echo "Installing the project's dependencies..."
	(rm -rf venv \
	&& python3 -m virtualenv venv \
	&& source venv/bin/activate \
	&& python3 -m pip install -r requirements/requirements-dev.txt \
	&& python3 -m pip install -r requirements/requirements-setup.txt \
	&& python3 -m pip install -r requirements/requirements-test.txt)
	@echo "The Project's environment is ready!!"

######################### End of User defined options ##########################

clean-coverage:
	rm -f .coverage
	rm -f coverage.xml

clean-build:
	rm -rf dist
	rm -rf skylla.egg-info
	rm -rf build

clean-test:
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -rf .mypy_cache

clean: clean-test clean-build clean-coverage

help:
	python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

mypy:
	mypy skylla

isort:
	isort --profile black skylla
	isort --profile black tests

lint-check:
	black --diff --color skylla
	@echo "\nUnused imports and variables are listed below:\n"
	autoflake -r skylla
	black --diff --color tests
	@echo "\nUnused imports and variables are listed below:\n"
	autoflake -r skylla

lint:
	black skylla
	autoflake -r -i skylla
	black tests
	autoflake -r -i tests

neat: isort lint mypy

test: neat ## run tests quickly with the default Python
	python3 -m pytest --cov=skylla --cov-report term-missing --ignore=setup.py -vvv

coverage: clean-coverage
	coverage run --source skylla -m pytest 
	coverage report -m
	coverage xml

printenv:
	printenv


build: clean-build
	python3 setup.py bdist_wheel

deploy: build ## Upload an release
	(printenv \
	&& python3 -m pip install --upgrade pip \
    && python3 -m pip install twine \
    && twine upload dist/*)