PY_DEPS := $(wildcard datapype/*.py)

dev: $(PY_DEPS)
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt -r requirements-dev.txt

test: dev
	tox

sdist: $(PY_DEPS)
	python setup.py sdist

pypi: sdist
	twine upload dist/*

clean:
	rm dist/*
	rm -r .venv
