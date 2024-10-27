# -*- coding:utf-8 -*-

"""
dir all tools in minghu6.tools
"""

from importlib import import_module

from minghu6.tools import find_tool_module_names


def show_doc(name: str):
    m = import_module("minghu6.tools." + name)

    return m.__doc__


def term_interactive():
    from simple_term_menu import TerminalMenu

    module_names = find_tool_module_names()

    module_menu = TerminalMenu(
        module_names,
        # ["abc", "def", "ghi"],
        menu_highlight_style=("bg_green", "bold", "underline"),
        title="Modules",
        cycle_cursor=True,
        raise_error_on_interrupt=True,
        preview_command=show_doc,
        preview_size=0.75,
    )

    module_menu.show()


if __name__ == "__main__":
    term_interactive()
