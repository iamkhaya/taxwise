mypy_files = taxwise/
devenv = PYTHONPATH=.
checkfiles = taxwise/ tests/ setup.py

help:
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    up          Updates dev/test dependencies"
	@echo  "    deps        Ensure dev/test dependencies are installed"
	@echo  "    lint	Reports all linter violations"
	@echo  "    test	Runs all tests"
	@echo  "    run         Runs in development mode"

up:
	pip-compile -v --rebuild
	pip-compile -U --no-index --no-emit-trusted-host requirements.in

deps:
	@pip3 install --upgrade pip
	@pip3 install -q pip-tools
	@pip-sync requirements.txt
	@pip3 install -qe .

isort:
	isort -rc $(checkfiles) tests

lint:
	flake8 $(checkfiles)
	pylint $(checkfiles)
	python setup.py check -mr

test:
	ROLE=TEST pytest --cov=taxwise --cov-report term tests


ci: lint test

run:
	python3 manage.py runserver

seed:
	python3 manage.py seed
