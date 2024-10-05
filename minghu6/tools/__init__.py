#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Only funny Appliacation can be here,
etc libary module file should be etc folder
"""

import os
import os.path as path

from public import public

from minghu6.etc.importer import walk_submodule_names
from minghu6.etc.version import iswin
from minghu6.itertools import flatten


@public
def find_tool_module_names() -> list[str]:

    excluded_names = ["cjg", "scaffold", "scaffold.leetcode"]

    if iswin():
        excluded_names.append("bump_version")

    return list(
        filter(
            lambda fn: fn not in excluded_names,
            flatten(map(lambda x: x[1] + x[2], walk_submodule_names(__name__))),
        )
    )
