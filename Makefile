PY_DEPS := $(wildcard datapype/*.py)

test: $(PY_DEPS) $(wildcard tests/*.py)
	tox

sdist: $(PY_DEPS)
	python setup.py sdist

pypi: sdist
	twine upload dist/*
