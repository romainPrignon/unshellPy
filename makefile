.PHONY: spec

src = unshell/
spec = spec/
report ?= term # or html

setup-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

install:
	poetry install
	./scripts/install_hooks.sh

dev: check

debug:
	poetry run pytest ${src} -x --pdb

lint:
	poetry run flake8 ${src} ${spec}

fmt:
	poetry run autopep8 --in-place --recursive ${src} ${spec}

check:
	poetry run mypy ${src}

test:
	poetry run pytest ${src}

test-file: ## make test-file f=unshell/test_core.py
	poetry run pytest ${f}

test-one: ## make test-one k=test_unshell_should_return_function
	poetry run pytest -k ${k}

spec:
	poetry run pytest ${spec}

cov:
	poetry run pytest --cov=${src} --cov=${spec} --cov-report=${report}

build: ## make build version=patch|minor|major
	rm -rf dist/
	poetry version ${version}
	poetry build

deploy:
	git add pyprojet.toml dist/
	git commit -m "Release $(shell poetry version -s)"
	git tag -a "$(shell poetry version -s)" -m "Release $(shell poetry version -s)"
	git push --follow-tags

publish:
	poetry publish

release: ## make release version=patch|minor|major
	gh workflow run release.yml -f version=${version} -f
