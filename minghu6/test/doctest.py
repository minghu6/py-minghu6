from doctest import run_docstring_examples
from importlib import import_module
from itertools import chain
from types import ModuleType
from typing import Callable, Generator, List, Union, Optional

from minghu6.etc.importer import list_submodule_names
from minghu6.functools import chain_apply, map, filter


def run_doctest(
    m: Union[ModuleType, str],
    onames: Optional[List[str]] = None,
    strict: bool = False,
    recursive: bool = False,
    verbose: bool = False,
):
    """strict: only test `__all__`
    or else find all function defined in the module

    :param oname: specific doc-obj names
    """

    if isinstance(m, str):
        m = import_module(m)

    def gather_subms(m: ModuleType) -> Generator[ModuleType, None, None]:
        mname = m.__name__

        def _gather_subms(m: str) -> Generator[str, None, None]:
            concat_names = lambda x: f"{m}.{x}"

            subpkgs, subms = list_submodule_names(m)

            yield from chain_apply(map(concat_names), subms)

            for subpkg in chain_apply(map(concat_names), subpkgs):
                yield subpkg
                yield from _gather_subms(subpkg)

        return chain_apply(
            map(lambda subm: import_module(subm)), _gather_subms(mname)
        )

    def gather_docobj(
        m: ModuleType, onames: Optional[List[str]], strict: bool
    ) -> Generator:
        mname = m.__name__

        if strict:
            docobj = chain_apply(
                map(lambda name: getattr(m, name)), getattr(m, "__all__", [])
            )
        else:
            docobj = chain_apply(
                filter(
                    lambda var: isinstance(var, Callable)
                    and getattr(var, "__module__", "") == mname
                ),
                map(lambda name: getattr(m, name)),
                dir,
                m,
            )

        if onames:
            docobj = chain_apply(filter(lambda x: x.__name__ in onames), docobj)

        return docobj

    def run_on_module(
        m: ModuleType, onames: Optional[List[str]], strict: bool, verbose: bool
    ):
        mname = m.__name__

        for docobj in gather_docobj(m, onames=onames, strict=strict):
            run_docstring_examples(
                docobj, m.__dict__, name=mname, verbose=verbose
            )

    ms = [m]

    if recursive:
        ms = chain(ms, gather_subms(m))

    for m in ms:
        run_on_module(m, onames=onames, strict=strict, verbose=verbose)
