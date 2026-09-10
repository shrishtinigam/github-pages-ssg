.PHONY: install check build test
PYTHON ?= python3
OUTPUT ?= ../pelican-output

install:
	$(PYTHON) -m pip install .

check:
	$(PYTHON) -m portfolio_cli check

build:
	$(PYTHON) -m portfolio_cli build --output "$(OUTPUT)"

test:
	$(PYTHON) -m unittest discover -s tests -v
