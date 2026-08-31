
[![PyPI version](https://badge.fury.io/py/minghu6.svg)](https://badge.fury.io/py/minghu6)
[![Build Status](https://travis-ci.org/minghu6/minghu6_py.svg?branch=develop)](https://travis-ci.org/minghu6/minghu6_py)
[![Coverage Status](https://coveralls.io/repos/github/minghu6/minghu6_py/badge.svg?branch=develop)](https://coveralls.io/github/minghu6/minghu6_py?branch=develop)



# An Utils Package

## Environment Setup

### 1. Configure Shell Environment Variables

Add these lines in bash startup profile.

```bash
export MINGHU6_HOME="<actual-dir-path>/minghu6_py"
export MINGHU6_SRC="$MINGHU6_HOME/minghu6"

export PATH="$PATH:$MINGHU6_SRC/tools/bin"

for file in $(pym6 find -p $MINGHU6_SRC/tools/bash-completion/ '*'); do
    . $file
done
```
### 2. Install Project Dependencies

Use `uv` as the project management tool.

`cd $MINGHU6_HOME && uv sync`
