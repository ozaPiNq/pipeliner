upload: clean
	python setup.py sdist
	twine upload dist/* -r pypi

clean:
	rm dist/* || true
