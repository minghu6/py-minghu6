import re
import random


INVALID_FILE_CHAR_SET = {"\\", "/", ":", "*", "?", '"', "<", ">", "|", "%", "&"}


def split_whitespace(src):
    src = src.strip()
    return re.split("\\s+", src)


def split_blankline(src):
    src = src.strip()
    return re.split("\\s+\n+", src)


def underscore(name, strict=False, case="lower"):
    """
    TODO: rewrite using hy
    >>> underscore('IOError')
    io_error
    >>> underscore('IOError', strict=True)
    i_o_error
    """
    if strict:
        word = re.sub("([A-Z])([A-Z](^[A-Z])*)", r"\1_\2", name)
        word = re.sub("([a-z0-9])([A-Z])", r"\1_\2", word)
        word = re.sub("([A-Z])([A-Z])", r"\1_\2", word)
    else:
        word = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        word = re.sub("([a-z0-9])([A-Z])", r"\1_\2", word)

    if case == "lower":
        word = word.replace("-", "_").lower()
    else:
        word = word.replace("-", "_").upper()

    return word


def camelize(name, upper_camel_case=True):
    name = name.replace("-", "_")
    components = name.split("_")
    if upper_camel_case:
        name = "".join(x.title() for x in components)
    else:  # lowerCamelCase
        name = components[0] + "".join(x.title() for x in components[1:])

    return name


def random_ascii_char() -> str:
    return bytes([random.randrange(0, 128)]).decode()


def random_ascii_string(length: int) -> str:
    return bytes((map(lambda _: random.randrange(0, 128), range(length)))).decode()
