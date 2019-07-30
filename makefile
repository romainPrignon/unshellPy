.PHONY: help install, freeze, lint, test, test-one, coverage, coverage-html, build
.SILENT: help install, freeze, lint, test, test-one, coverage, coverage-html, build

help: ## make help
	python setup.py --help-command

install: ## make install
	pip install -r requirements.txt
	./scripts/install_hooks.sh

freeze: # make freeze
	pip freeze > requirements.txt

lint: ## make lint
	flake8 src/ type/
	mypy src/ type/

test: ## make test
	python setup.py test

test-one: ## make test test=src.test_unshell.TestUnshell.test_unshell_should_return_function
	python setup.py test --test-suite $(test)

coverage: ## make coverage
	coverage run setup.py test
	coverage report -m

coverage-html: ## make coverage-html
	coverage html

build:
	python setup.py bdist bdist_wheel
