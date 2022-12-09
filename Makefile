SHELL:=/usr/bin/env bash

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

