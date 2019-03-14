test:
	echo 'todo'

sdist:
	python setup.py sdist

pypi:
	twine upload dist/*

clean:
	rm dist/*
