import os
from setuptools import find_packages, setup
import minghu6

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='minghu6',
    version=minghu6.__version__,
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['captcha=minghu6.tools.captcha.__main__:cli',
                            'ffmpeg-fix=minghu6.tools.ffmpeg_fix:cli',
                            # 'file_monitor=minghu6.tools.file_monitor:cli', #ONLY WINDOWS UPTONOW
                            'fileformat=minghu6.tools.fileformat:cli',
                            'launch=minghu6.tools.launch:cli',
                            'proxy-ip=minghu6.tools.proxy_ip:cli',
                            'yinyuetai=minghu6.tools.yinyuetai:cli',
                            'text-editor=minghu6.tools.text_editor:cli',
                            'youtube=minghu6.tools.youtube:cli',
                            'lc=minghu6.tools.lc:cli',
                            'add-pypath=minghu6.tools.add_pypath:cli',
                            'tieba=minghu6.tools.tieba:cli',
                            'head-py=minghu6.tools.head:cli',
                            'tail-py=minghu6.tools.tail:cli',
                            'text-py=minghu6.tools.text:cli',
                            'find_max-py=minghu6.tools.find_max:cli',
                            'find-py=minghu6.tools.find:cli',
                            'timeme=minghu6.tools.timeme:cli'
                            ],
    },
    include_package_data=True,
    license='BSD License',
    description='minghu6 Util Package',
    long_description=README,
    url='https://github.com/minghu6/minghu6_py',
    author='minghu6',
    author_email='a19678zy@163.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
