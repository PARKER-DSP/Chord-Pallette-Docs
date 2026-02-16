.PHONY: docs-nav docs-check docs-build docs-serve docs-ci

docs-nav:
	python tools/docs_tool.py generate-nav

docs-check:
	python tools/docs_tool.py check-all

docs-build:
	python tools/docs_tool.py build

docs-serve:
	python tools/docs_tool.py serve

docs-ci:
	python tools/docs_tool.py ci
