.PHONY: help dev, lint, test, build
.SILENT: help dev, lint, test, build

help: ## make help
	python setup.py --help-command

install: ## make install
	pip install -r requirements.txt

freeze: # make freeze
	pip freeze > requirements.txt

lint: ## make lint
	flake8 src/ type/
	mypy src/

test: ## make test [module=src.test_unshell.TestUnshell.test_unshell_should_return_function]
	python -m unittest $(module)

build:
	python setup.py bdist bdist_wheel
