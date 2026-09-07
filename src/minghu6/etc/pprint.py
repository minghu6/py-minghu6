

def format_int(n: int, seg: int, delimiter: str) -> str:
    if seg <= 0:
        raise ValueError('seg should be at least 1')

    l = [
        c + delimiter if (i) % seg == 0 else c
        for i, c in enumerate(reversed(str(n)))
    ]

    return "".join(l[::-1])[:-1]
