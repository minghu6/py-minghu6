import ast
import shutil
from packaging.version import Version

import minghu6
from minghu6.etc.cmd import exec_cmd, mkstempfile
from minghu6.etc.importer import check_module
from minghu6.tools.bump_version import App


def format_code(code: str) -> str:
    class NoProperFormatterError(Exception):
        pass

    if shutil.which("black"):
        with mkstempfile() as fn:
            with open(fn, mode="w") as fw:
                fw.write(code)

            exec_cmd(f'black "{fn}"')

            with open(fn, mode="r") as fr:
                return fr.read()

    autopep8 = check_module("autopep8")

    if autopep8:

        return autopep8.fix_code(code)

    raise NoProperFormatterError("install [black (recommend) | autopep8]")


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
