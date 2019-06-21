.PHONY: dev, build, test
.SILENT: dev, build, test

dev: ## make dev script=./fixtures/scripts/my_script.py [args="foo bar"]
	docker run --name unshell-py -it --rm -v ${shell pwd}/src:/opt/src unshell-py python src/cli.py $(script) $(args)

build:
	docker build -t unshell-py .

test:
	docker run --name unshell-py -it --rm -v ${shell pwd}/src:/opt/src -v ${shell pwd}/tests:/opt/tests unshell-py python -m unittest
