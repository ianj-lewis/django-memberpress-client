# -------------------------------------------------------------------------
# build a package for PyPi
# -------------------------------------------------------------------------
.PHONY: build requirements deps-update deps-init

db:
	mysql -uroot -p < memberpress_client/scripts/init-db.sql

up:
	brew services start mysql
	brew services start redis

down:
	brew services stop mysql
	brew services stop redis

server:
	./manage.py runserver 0.0.0.0:8000

migrate:
	./manage.py migrate
	./manage.py makemigrations memberpress_client
	./manage.py migrate memberpress_client

requirements:
	pip-compile requirements/common.in
	pip-compile requirements/local.in
	pip install -r requirements/common.txt
	pip install -r requirements/local.txt

report:
	cloc $(git ls-files)

shell:
	./manage.py shell_plus


quickstart:
	pre-commit install
	make requirements
	make up
	make db
	make migrate
	./manage.py createsuperuser
	make server

test:
	./manage.py test

build:
	python3 -m pip install --upgrade setuptools wheel twine
	python -m pip install --upgrade build

	if [ -d "./build" ]; then sudo rm -r build; fi
	if [ -d "./dist" ]; then sudo rm -r dist; fi
	if [ -d "./django_memberpress_client.egg-info" ]; then sudo rm -r django_memberpress_client.egg-info; fi

	python3 -m build --sdist ./
	python3 -m build --wheel ./

	python3 -m pip install --upgrade twine
	twine check dist/*


deps-init:
	rm -rf .tox
	python -m pip install --upgrade pip wheel
	pwd
	python -m pip install --upgrade -r requirements/common.txt -r requirements/local.txt -e .
	python -m pip check

deps-update:
	pre-commit autoupdate
	python -m pip install --upgrade pip-tools pip wheel
	python -m piptools compile --upgrade --resolver backtracking -o ./requirements/common.txt pyproject.toml
	python -m piptools compile --extra dev --upgrade --resolver backtracking -o ./requirements/local.txt pyproject.toml

# -------------------------------------------------------------------------
# upload to PyPi Test
# https:// ?????
# -------------------------------------------------------------------------
release-test:
	make build
	twine upload --skip-existing --repository testpypi dist/*


# -------------------------------------------------------------------------
# upload to PyPi
# https://pypi.org/project/django-memberpress-client/
# -------------------------------------------------------------------------
release-prod:
	make build
	twine upload --skip-existing dist/*
