build_distribution:
	python setup.py sdist bdist_wheel

upload_to_testpypi:
	twine upload --repository testpypi dist/* --verbose

upload_to_pypi:
	twine upload dist/*