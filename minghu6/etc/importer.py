# -*- coding:utf-8 -*-

import re
import os

from importlib import import_module
from pathlib import Path
from types import ModuleType
from collections.abc import Generator

from minghu6.itertools import flattenall
from minghu6.meta.var import find_attrs


def check_module(module_name) -> ModuleType:
    try:
        return import_module(module_name)
    except ImportError:
        pass


def auto_load_var(package_name, module_pattern, variable_pattern, base_path=None):
    """auto_load_var('minghu6.etc', 'fi.*', '[f|F].*')

    [<function minghu6.etc.find.find>,
     <function minghu6.etc.find.findlist>,
     <module 'fnmatch' from '/usr/lib/python3.5/fnmatch.py'>,
     minghu6.etc.fileformat.FileTypePair,
     <function minghu6.etc.fileformat.fileformat>]
    """

    def find_module_names(base_path, pattern):
        return [
            os.path.splitext(fn)[0]
            for fn in os.listdir(base_path)
            if re.match(pattern, os.path.splitext(fn)[0])
        ]

    def load_var_from_module(module_name, attrname_pattern):
        """get all attrtibute according to name pattern
        from a module(import from module name)
        """
        try:
            module = import_module(module_name)
        except ImportError:
            return []
        else:
            return find_attrs(module, attrname_pattern)

    if base_path is None:
        base_path = package_name.replace(".", os.sep)

    return list(
        flattenall(
            map(
                lambda module_name: load_var_from_module(
                    "%s.%s" % (package_name, module_name), variable_pattern
                ),
                find_module_names(base_path, module_pattern),
            )
        )
    )


def list_submodule_names(m: ModuleType | str) -> tuple[list[str], list[str]]:
    """
    -> (package_names, module_names)

    NOTE: Current implementation just ignore the Namespace case.
    """

    if isinstance(m, str):
        m = import_module(m)

    if not hasattr(m, '__path__'):
        return ([], [])

    package_names = []
    module_names = []

    for pypath in getattr(m, '__path__'):
        for file in Path(pypath).iterdir():
            fn = file.name

            if file.is_file():
                if fn.endswith(".py") and fn != "__init__.py":
                    module_names.append(fn[:-3])

            elif file.is_dir():
                if file.joinpath("__init__.py").exists():
                    package_names.append(fn)

    return (package_names, module_names)


def walk_submodule_names(m: ModuleType | str) -> Generator[(str, str, str)]:
    """ topdown walk (root, packages, modules) """

    if isinstance(m, ModuleType):
        mname = m.__name__
    else:
        mname = m

    subpnames, submnames = list_submodule_names(m)

    yield (mname, subpnames, submnames)

    for pname in subpnames:
        yield from walk_submodule_names(f"{mname}.{pname}")


if __name__ == "__main__":
    check_module("1234", "1234")
