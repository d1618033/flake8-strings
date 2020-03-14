.PHONY: init test lint pretty precommit_install bump_major bump_minor bump_patch

BIN = .venv/bin/
CODE = flake8_strings

init:
	python3 -m venv .venv
	poetry install

test:
	poetry run pytest --verbosity=2 --showlocals --strict --log-level=DEBUG --cov=$(CODE) $(args)

lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE) tests
	poetry run pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE) tests
	poetry run black --skip-string-normalization --check $(CODE) tests
	poetry run pytest --dead-fixtures --dup-fixtures

pretty:
	poetry run isort --apply --recursive $(CODE) tests
	poetry run black --skip-string-normalization $(CODE) tests
	poetry run unify --in-place --recursive $(CODE) tests

precommit_install:
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

bump_major:
	poetry run bumpversion major

bump_minor:
	poetry run bumpversion minor

bump_patch:
	poetry run bumpversion patch