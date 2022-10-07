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
	pip install -q pip-tools
	pip-compile -v --rebuild
	pip-compile -U --no-emit-index-url --no-emit-trusted-host requirements.in
	pip-compile -U --no-emit-index-url --no-emit-trusted-host tests/requirements.in

deps:
	@pip3 install --upgrade pip
	@pip3 install -q pip-tools
	@pip-sync requirements.txt tests/requirements.txt
	@pip3 install -qe .

isort:
	isort -rc $(checkfiles) tests

lint:
	flake8 $(checkfiles)
	pylint $(checkfiles)
	python setup.py check -mr

style:
	isort $(checkfiles)
	black $(checkfiles)

test:
	ROLE=TEST pytest --cov=taxwise --cov-report term tests


ci: lint test

run:
	python3 manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations --verbosity 3 
	
mergemigrations:
	python manage.py makemigrations --verbosity 3 --merge 

seed:
	python3 manage.py seed
