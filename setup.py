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
	version = '1.3.0',
	install_requires = required,
	packages = find_packages(),
	entry_points = {
        'console_scripts' : ['captcha=minghu6.tools.captcha:interactive',
                             'ffmpeg_fix=minghu6.tools.ffmpeg_fix:interactive',
                             'fileformat=minghu6.tools.fileformat:interactive',
                             'launch=minghu6.tools.launch:interactive',
                             'proxy_ip=minghu6.tools.proxy_ip:interactive',
                             'yinyuetai=minghu6.tools.Tai_downloader:interactive',
                             'text_editor=minghu6.tools.textEditor:interactive',
                             'youtube=minghu6.tools.Tube_downloader:interactive',
                             'countlines=minghu6.tools.count_lines:interactive',
                             'add_pypath=minghu6.tools.add_py_path:interactive',
                             'tieba=minghu6.tools.Tieba_downloader:interactive',
                             ],
    },
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
