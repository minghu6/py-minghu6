#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Only funny Appliacation can be here,
etc libary module file should be etc folder
"""

import os
import os.path as path
from typing import List

from public import public

from minghu6.etc.version import iswin


@public
def get_module_names() -> List[str]:
    curpath = path.dirname(__file__)

    def _find_module_names(dirpath: str) -> List[str]:
        module_names = []

        for fn in os.listdir(dirpath):
            if fn.endswith(".py") and fn != "__init__.py":
                module_names.append(fn[:-3])

            # check if it's a folder module
            elif path.isdir(path.join(curpath, fn)):
                subdirpath = path.join(curpath, fn)

                if path.exists(path.join(subdirpath, "__init__.py")):
                    module_names.append(fn)

                    module_names.extend(
                        map(lambda name: f"{fn}.{name}", _find_module_names(subdirpath))
                    )

        return module_names

    excluded_names = ["cjg", "scaffold", "scaffold.leetcode"]

    if iswin():
        excluded_names.append("bump_version")

    return list(
        filter(
            lambda fn: fn not in excluded_names,
            _find_module_names(curpath)
        )
    )
