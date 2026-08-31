#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Only funny Appliacation can be here,
etc libary module file should be etc folder
"""

from exports import export

from minghu6.etc.importer import walk_submodule_names
from minghu6.etc.version import iswin
from minghu6.itertools import flatten
from minghu6.functools import map, filter, chain, chain_apply


@export
def find_tool_module_names() -> list[str]:

    excluded_names = ["scaffold"]

    if iswin():
        excluded_names.append("bump_version")

    # print(
    #     chain_apply(
    #         list,
    #         map(lambda p: p.removeprefix("minghu6.tools.")),
    #         flatten,
    #         map(
    #             lambda x: chain_apply(
    #                 map(lambda y: f"{x[0]}.{y}"), chain(x[2]), x[1]
    #             )
    #         ),
    #         walk_submodule_names(__name__),
    #     )
    # )

    return chain_apply(
        list,
        filter(lambda fn: fn not in excluded_names),
        map(lambda p: p.removeprefix("minghu6.tools.")),
        flatten,
        map(
            lambda x: chain_apply(
                map(lambda y: f"{x[0]}.{y}"), chain(x[2]), x[1]
            )
        ),
        walk_submodule_names(__name__),
    )
