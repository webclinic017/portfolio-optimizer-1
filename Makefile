PROJECT_NAME = portfolio-optimization
PYTHON_VERSION = 3.9.7

.ONESHELL:
.PHONY: pyenv-new pyenv clean lint update-pip update-poetry requirements update run

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
	black portfolio_optimization/
	isort --profile black portfolio_optimization/

update-pip:
	pip install -U pip

update-poetry:
	poetry update

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

update: update-pip update-poetry requirements

run:
	uvicorn --factory portfolio_optimization.app:create_app --reload --host 0.0.0.0 --port 5000
