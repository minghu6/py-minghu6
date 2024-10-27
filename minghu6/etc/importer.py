# -*- coding:utf-8 -*-

from importlib import import_module
from pathlib import Path
from types import ModuleType
from collections.abc import Iterator


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


def walk_submodule_names(m: ModuleType | str) -> Iterator[tuple[str, str, str]]:
    """ topdown walk (root, packages, modules) """

    if isinstance(m, ModuleType):
        mname = m.__name__
    else:
        mname = m

    subpnames, submnames = list_submodule_names(m)

    yield (mname, subpnames, submnames)

    for pname in subpnames:
        yield from walk_submodule_names(f"{mname}.{pname}")
