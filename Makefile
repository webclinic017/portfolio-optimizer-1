PROJECT_NAME = portfolio-optimizer
PYTHON_VERSION = 3.9.7

.ONESHELL:
.PHONY: pyenv-new pyenv clean lint update-pip update-poetry requirements update run build

pyenv-new:
	pyenv virtualenv $(PYTHON_VERSION) $(PROJECT_NAME)
	pyenv local $(PROJECT_NAME)
	poetry install -v

pyenv: clean pyenv-new requirements

clean:
	rm requirements.txt || true
	pyenv local --unset
	pyenv uninstall -f $(PROJECT_NAME)

lint:
	black portfolio_optimizer/
	isort --profile black portfolio_optimizer/

update-pip:
	pip install -U pip

update-poetry:
	poetry update

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

update: update-pip update-poetry requirements

run:
	python -m portfolio_optimizer

build: requirements
	docker build -f Dockerfile -t eserdk/portfolio-optimizer:latest .
