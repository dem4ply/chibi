.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -Rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr coverage_html_report/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 chibi_4chan tests

coverage: ## check code coverage quickly with the default Python
	coverage run --source chibi_4chan setup.py test
	coverage report -m
	coverage html
	$(BROWSER) coverage_html_report/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/chibi_4chan.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ chibi_4chan
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python -m build
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

report:
	@coverage report
	@coverage html

test_unit:
	@echo "Running tests"
	@export PYTHON_UNITTEST_LOGGER=WARNING; \
		coverage run -m unittest discover -p "*.py" -s tests

open_report_firefox:
	@nohup firefox .coverage_html_report/index.html > /dev/null &

pep8:
	@echo "Running pep8 tests..."
	@pycodestyle --statistics chibi tests

flakes:
	@echo "Running flakes tests..."
	@flake8 chibi tests

test: test_unit report

style_test: flakes pep8
