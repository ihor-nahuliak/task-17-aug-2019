.PHONY: clean install test

DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL=/bin/bash

GLOBAL_PYTHON = /usr/bin/python3.7
ENV := $(DIR)/env/bin
PYTHON := $(ENV)/python
PIP := $(ENV)/pip
FLAKE8 := $(ENV)/flake8
COVERAGE := $(ENV)/coverage

STATUS_ERROR := \033[1;31m*\033[0m Error
STATUS_OK := \033[1;32m*\033[0m OK


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} + ;\
	find . -name '*.pyo' -exec rm -f {} + ;\
	find . -name '*~' -exec rm -f {} + ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

clean: clean-pyc


install-env-python:
	rm -rf "$(DIR)/env/" ;\
	virtualenv -p $(GLOBAL_PYTHON) --clear "$(DIR)/env/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

env-activate:
	. $(ENV)/activate

install-python-libs:
	$(PIP) install -U pip ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements.txt" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install: install-env-python env-activate install-python-libs


test-flake8:
	@$(FLAKE8) --config="$(DIR)/.flake8rc" "$(DIR)/app" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "Flake8: ${STATUS_OK}" ;\
	else \
		echo -e "Flake8: ${STATUS_ERROR}" ;\
	fi;

test-django:
	@$(COVERAGE) run --source="$(DIR)/app" "$(DIR)/app/manage.py" test ;\
	if [ $$? -eq 0 ]; then \
		echo -e "Tested: ${STATUS_OK}" ;\
	else \
		echo -e "Tested: ${STATUS_ERROR}" ;\
	fi;

test-coverage:
	@$(COVERAGE) report -m && \
	$(COVERAGE) html ;\
	if [ $$? -eq 0 ]; then \
		echo -e "Coverage: ${STATUS_OK}" ;\
	else \
		echo -e "Coverage: ${STATUS_ERROR}" ;\
	fi;

test: test-flake8 test-django test-coverage
