
import ast
from packaging.version import Version

import minghu6
from minghu6.tools.bump_version import App


def hook_version_inc(version: Version):
    mod = ast.parse(open(minghu6.__file__).read())

    for node in ast.walk(mod):
        if isinstance(node, ast.Assign):
            for name in node.targets:
                if name.id == '__version__':
                    node.value.value = str(version)

    open(minghu6.__file__, 'w').write(ast.unparse(mod))


if __name__ == '__main__':

    App(hook_version_inc).run()

