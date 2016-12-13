import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()
with open('requirements.txt') as f:
	required = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name = 'minghu6',
	version = '1.0.6',
	install_requires = required,
	packages = find_packages(),
	include_package_data = True,
	license = 'BSD License', 
	description = 'A Core Utils Set for minghu6.',
	long_description = README,
	url = 'https://github.com/minghu6/minghu6_py',
	author = 'minghu6',
	author_email = 'a19678zy@163.com',
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
	)
