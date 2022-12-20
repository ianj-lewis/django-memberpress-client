# -------------------------------------------------------------------------
# build a package for PyPi
# -------------------------------------------------------------------------
.PHONY: build requirements deps-update deps-init

dev-db:
	mysql -uroot -p < memberpress_client/scripts/init-db.sql

dev-up:
	brew services start mysql
	brew services start redis

dev-down:
	brew services stop mysql
	brew services stop redis

django-server:
	./manage.py runserver 0.0.0.0:8000

django-migrate:
	./manage.py migrate
	./manage.py makemigrations memberpress_client
	./manage.py migrate memberpress_client

django-shell:
	./manage.py shell_plus


django-quickstart:
	pre-commit install
	make requirements
	make dev-up
	make dev-db
	make django-migrate
	./manage.py createsuperuser
	make django-server

django-test:
	./manage.py test

requirements:
	pre-commit autoupdate
	python3 -m pip install --upgrade pip wheel
	pip-compile requirements/common.in
	pip-compile requirements/local.in
	pip install -r requirements/common.txt
	pip install -r requirements/local.txt

deps-init:
	rm -rf .tox
	python3 -m pip install --upgrade pip wheel
	python3 -m pip install --upgrade -r requirements/common.txt -r requirements/local.txt -e .
	python3 -m pip check

deps-update:
	python3 -m pip install --upgrade pip-tools pip wheel
	python3 -m piptools compile --upgrade --resolver backtracking -o ./requirements/common.txt pyproject.toml
	python3 -m piptools compile --extra dev --upgrade --resolver backtracking -o ./requirements/local.txt pyproject.toml


report:
	cloc $(git ls-files)


build:
	python3 -m pip install --upgrade setuptools wheel twine
	python3 -m pip install --upgrade build

	if [ -d "./build" ]; then sudo rm -r build; fi
	if [ -d "./dist" ]; then sudo rm -r dist; fi
	if [ -d "./django_memberpress_client.egg-info" ]; then sudo rm -r django_memberpress_client.egg-info; fi

	python3 -m build --sdist ./
	python3 -m build --wheel ./

	python3 -m pip install --upgrade twine
	twine check dist/*


# -------------------------------------------------------------------------
# upload to PyPi Test
# https:// ?????
# -------------------------------------------------------------------------
release-test:
	make build
	twine upload --verbose --skip-existing --repository testpypi dist/*


# -------------------------------------------------------------------------
# upload to PyPi
# https://pypi.org/project/django-memberpress-client/
# -------------------------------------------------------------------------
release-prod:
	make build
	twine upload --verbose --skip-existing dist/*
