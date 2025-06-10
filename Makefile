.PHONY: test lint build

test:
	pytest tests/

lint:
	flake8 src/
	mypy src/

build:
	docker build -t mlops-pipeline-app .