SHELL:=/usr/bin/env bash

.PHONY: crawl
crawl:
	python airbnb_spider/run_spider.py

.PHONY: web
web:
	python web/app.py  $(filter-out $@, $(MAKECMDGOALS))

.PHONY: convert
convert:
	python web/convert.py $(filter-out $@, $(MAKECMDGOALS))

.PHONY: data
data:
	python web/data.py $(filter-out $@, $(MAKECMDGOALS))

# avoid "/bin/sh: sphinx-build: command not found" error for convert
%:
	@:

.PHONY: lint
lint:
	poetry run mypy airbnb_spider tests/**/*.py
	poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	echo "WARNING: safety check are disabled"
	# poetry run safety check --full-report

.PHONY: test
test: lint package unit

.DEFAULT:
	@cd docs && $(MAKE) $@

