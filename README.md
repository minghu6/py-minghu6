
[![PyPI version](https://badge.fury.io/py/minghu6.svg)](https://badge.fury.io/py/minghu6)
[![Build Status](https://travis-ci.org/minghu6/minghu6_py.svg?branch=develop)](https://travis-ci.org/minghu6/minghu6_py)
[![Coverage Status](https://coveralls.io/repos/github/minghu6/minghu6_py/badge.svg?branch=develop)](https://coveralls.io/github/minghu6/minghu6_py?branch=develop)



# An Utils Package

## Install

### Install from local

`python ./lvse_install/auto_install.py`

#### Setup tools environments

Add these lines in bash startup profile

```bash
MINGHU6_HOME=$(python -m minghu6.tools.introspect minghu6_home)

export PATH="$PATH:$MINGHU6_HOME/tools/bin"

for file in $(pym6 find -p $MINGHU6_HOME/tools/bash-completion/ '*'); do
    . $file
done
```
