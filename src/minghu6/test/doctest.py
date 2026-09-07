from doctest import run_docstring_examples
from importlib import import_module
from itertools import chain
from types import ModuleType
from collections.abc import Callable, Generator

from minghu6.etc.importer import list_submodule_names
from minghu6.functools import compose, fmap, keep


def run_doctest(
    m: ModuleType | str,
    onames: list[str] | None = None,
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

            yield from compose(fmap(concat_names), subms)

            for subpkg in compose(fmap(concat_names), subpkgs):
                yield subpkg
                yield from _gather_subms(subpkg)

        return compose(
            fmap(lambda subm: import_module(subm)), _gather_subms(mname)
        )

    def gather_docobj(
        m: ModuleType, onames: list[str] | None, strict: bool
    ) -> Generator:
        mname = m.__name__

        if strict:
            docobjs = compose(
                fmap(lambda name: getattr(m, name)), getattr(m, "__all__", [])
            )
        else:
            docobjs = compose(
                keep(
                    lambda var: isinstance(var, Callable)
                    and getattr(var, "__module__", "") == mname
                ),
                fmap(lambda name: getattr(m, name)),
                dir,
                m,
            )

        if onames:
            docobjs = compose(
                keep(
                    lambda obj: any(
                        fmap(lambda name: name in obj.__name__)(onames)
                    )
                ),
                docobjs,
            )

        return docobjs

    def run_on_module(
        m: ModuleType, onames: list[str] | None, strict: bool, verbose: bool
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
