PROJECT_NAME = portfolio-optimization
PYTHON_VERSION = 3.9.6

pyenv:
	make clean
	pyenv virtualenv $(PYTHON_VERSION) $(PROJECT_NAME)
	pyenv local $(PROJECT_NAME)
	poetry install -v

clean:
	pyenv local --unset
	pyenv uninstall -f $(PROJECT_NAME)

update:
	pip install -U pip
	poetry update
