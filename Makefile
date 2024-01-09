.ONESHELL:
setup: style

style:
	flake8 .
	black . --check --diff
	cd advanote
	python manage.py test
