
PYTHON=python

bumpversion:
	$(PYTHON) ./bump_version.py

unittest:
	nose2

envtest:
	tox
