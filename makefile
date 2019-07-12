.PHONY: dev, build, test
.SILENT: dev, build, test

dev: ## make dev script=./fixtures/scripts/my_script.py [args="foo bar"]
	docker run --name unshell-py -it --rm -v ${shell pwd}:/opt unshell-py python src/cli.py $(script) $(args)

build:
	docker build -t unshell-py .

test: ## make test [module=src.test_unshell.TestUnshell.test_unshell_should_return_function]
	docker run --name unshell-py -it --rm -v ${shell pwd}:/opt unshell-py python -m unittest $(module)
