

from pprint import pprint


def format_int(n: int, seg: int, delimiter: str) -> str:
    assert seg > 0

    l = [
        c + delimiter if (i) % seg == 0 else c
        for i, c in enumerate(reversed(str(n)))
    ]

    return "".join(l[::-1])[:-1]
