#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Only funny Appliacation can be here,
etc libary module file should be etc folder
"""

from itertools import chain

from exports import export

from minghu6.etc.importer import walk_submodule_names
from minghu6.etc.version import iswin
from minghu6.itertools import flatten
from minghu6.functools import flow, fmap, keep, compose


@export
def find_tool_module_names() -> list[str]:

    excluded_names = ["scaffold"]

    if iswin():
        excluded_names.append("bump_version")

    return compose(
        list,
        keep(lambda fn: fn not in excluded_names),
        fmap(lambda p: p.removeprefix("minghu6.tools.")),
        flatten,
        fmap(lambda x: map(lambda y: f"{x[0]}.{y}", chain(x[1], x[2]))
        ),
        walk_submodule_names(__name__),
    )
