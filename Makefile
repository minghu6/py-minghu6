
PYTHON=python

bumpversion:
	$(PYTHON) ./bump_version.py

unittest:
	nose2

doctest:
	@ $(PYTHON) -m minghu6.tools.doctest minghu6 -r

envtest:
	tox
