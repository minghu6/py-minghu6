import ast
from importlib import import_module
import shutil
from packaging.version import Version

import minghu6
from minghu6.cmd import wait_run, mkstempfile
from minghu6.tools.bump_version import App


def format_code(code: str) -> str:
    class NoProperFormatterError(Exception):
        pass

    if shutil.which("black"):
        with mkstempfile() as fn:
            with open(fn, mode="w") as fw:
                fw.write(code)

            wait_run(f'black "{fn}"')

            with open(fn, mode="r") as fr:
                return fr.read()

    try:
        autopep8 = import_module('autopep8')
    except ImportError as ex:
        raise NoProperFormatterError(
            "install [black (recommend) | autopep8]"
            ) from ex
    else:
        return autopep8.fix_code(code)


def hook_version_inc(version: Version):
    mod = ast.parse(open(minghu6.__file__).read())

    for node in ast.walk(mod):
        if isinstance(node, ast.Assign):
            for name in node.targets:
                if name.id == "__version__":
                    node.value.value = str(version)

    open(minghu6.__file__, "w").write(format_code(ast.unparse(mod)))


if __name__ == "__main__":

    App(hook_version_inc).run()
