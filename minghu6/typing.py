""" Basicly a clone from stdlib _typeshed """

from os import PathLike

type StrPath = str | PathLike[str]                                   # stable
type BytesPath = bytes | PathLike[bytes]                             # stable
type StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]  # stable
