# -*- coding:utf-8 -*-

import re
import os

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from io import IOBase, StringIO, TextIOBase
from pathlib import Path
from functools import singledispatchmethod
from typing import Iterable, Self

from exports import export
from more_itertools import peekable

from minghu6.typing import StrPath
from minghu6.data import duplicated
from minghu6.functools import compose, keep


#################################################################################
#### Boostrap

class State(Enum):
    ESCAPE = auto()
    NORMAL = auto()


class EscapeRule:

    def __init__(self, escapechar: str) -> None:
        if len(escapechar) != 1:
            raise ValueError(f"{escapechar} is not a char")

        self.escapechar = escapechar

    def escape(self, specialchars: str, raw: str) -> str:
        if self.escapechar not in specialchars:
            raise ValueError(f"escapechar: `{self.escapechar}` should "
                             f"belong to specialchars: {specialchars}")

        dupchars = duplicated(specialchars)

        if dupchars:
            raise ValueError(f"duplicate chars `{dupchars}`"
                             f" in specialchars {specialchars}")

        escaped = []

        for c in raw:
            if c in specialchars:
                escaped.append(self.escapechar)

            escaped.append(c)

        return ''.join(escaped)

    def unescape(self, escaped: str) -> str:
        raw = []

        state = State.NORMAL

        for c in escaped:
            match (c, state):
                case (c0, State.NORMAL) if c0 == self.escapechar:
                    state = State.ESCAPE
                case (_, State.NORMAL):
                    raw.append(c)
                case (_, State.ESCAPE):
                    raw.append(c)
                    state = State.NORMAL

        if state is State.ESCAPE:
            raise ValueError(f"invalid str `{escaped}`"
                             f" endswith `{self.escapechar}`")

        return ''.join(raw)

    def split(
        self,
        escaped: str,
        sep: str,
        # pairs: list[tuple[str, str]] = []
    ) -> list[str]:
        """
        :sep: single char
        :pairs: word boundary (left, right) such as `("'", "'")`"`
        >>>
        """

        if len(sep) > 1:
            raise ValueError(
                f"unsupport multiple char seperator `{sep}`"
            )

        if len(sep) == 0:
            raise ValueError("empty separator")

        res = []

        state = State.NORMAL
        j = 0

        for i, c in enumerate(escaped):
            match (c, state):
                case (c0, State.NORMAL) if c0 == self.escapechar:
                    state = State.ESCAPE
                case (_, State.NORMAL):
                    if c == sep:
                        res.append(escaped[j:i])
                        j = i
                case (_, State.ESCAPE):
                    state = State.NORMAL

        res.append(escaped[j:])

        return res


#################################################################################
#### Contants

PROTECED_SEC = r'_.*'
SEC_SEP = "_sep"
DEFAULT_SEP = ' '
ESCAPE_RULE = EscapeRule('\\')
SPECIALCHARS = '[]\\'


class Bracket(StrEnum):
    LEFT = '['
    RIGHT = ']'


#################################################################################
#### Main

@export
@dataclass
class Section:
    name: str
    data: list[list[str]]

    def __bool__(self) -> bool:
        return bool(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class Mode(Enum):
    RW = auto(),
    W = auto()


W = Mode.W
RW = Mode.RW

export('W')
export('RW')


def _apply_index_args(obj, idx):
    if not isinstance(idx, tuple):
        return obj[idx]

    subo = obj

    for subi in idx:
        subo = subo[subi]

    return subo


@dataclass
class SmallConfigData:
    sections: dict[str, Section]
    sep: str


@export
class SmallConfig:
    """
    Line based config file which can be considered as

    `multiline .ini` file
    or `sectioned .csv` file

    Both for human and machine read and write
    ```
    # top three sections
    [_sep]
    %20

    [last_time]
    2017-01-01 10:02

    [failed]
    545321 http://csdn.com/postid#!=545321
    632222 http://csdn.com/postid#!=632222
    ```
    """

    def __init__(self, fpath: StrPath, mode: Mode, sep: str = DEFAULT_SEP, strict: bool = True):
        """ Create a new SmallConfig object on file"""

        self.fpath = Path(fpath)

        if not isinstance(mode, Mode):
            raise ValueError(f"invalid mode {mode}")

        self.strict = strict

        if mode is Mode.RW:
            if not self.fpath.exists():
                raise FileNotFoundError(self.fpath)

            with self.fpath.open('r') as f:
                data = StreamParser(
                    f,
                    sep = sep,
                    strict = self.strict
                ).parse()

            self._sections = data.sections
            self._sep = data.sep

        else:
            self._sections = {}
            self._sep = DEFAULT_SEP

    def _as_data(self) -> SmallConfigData:
        return SmallConfigData(
            sections=self._sections,
            sep=self._sep
        )

    def sections(self) -> Iterable[Section]:
        """get a user sections (_ excluded)"""
        return compose(
            keep(lambda x: not re.match(PROTECED_SEC, x.name)),
            self._sections.values()
        )

    def append(self, section: Section) -> Section:
        name = section.name

        if name in self._sections:
            raise ValueError(f"key {name} exist")

        if re.match(PROTECED_SEC, name):
            raise ValueError(f"proteced key {name}")

        self._sections[name] = section

        return self._sections[name]

    def pop(self, name: str) -> Section:
        if re.match(PROTECED_SEC, name):
            raise ValueError(f"proteced key {name}")

        self._sections.pop(name)

    def sync(self) -> int:
        """ sync data into persistent storage"""

        strbuf = StringIO()

        Unparser(
            self._as_data(),
            strbuf,
            strict=self.strict
        ).unparse()

        # on guard above

        with self.fpath.open('w') as f:
            cnt = f.write(strbuf.getvalue())

        return cnt

    def __contains__(self, name):
        return name in self._sections

    def __getitem__(self, idx) -> Section | list[str] | str:
        return _apply_index_args(self._sections, idx)

    def __setitem__(self, idx: str, value: Section):
        """ return old """

        if idx != value.name:
            raise ValueError(
                f"name conflicts for {idx} and {value}"
            )

        old = self._sections[idx]

        self._sections[idx] = value

        return old

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_):
        self.sync()


#################################################################################
#### Parser & Unparser

class SyntaxError(Exception): pass
class SemanticsError(Exception): pass


class Line: pass


@dataclass
class SectionName(Line):
    name: str


@dataclass
class StrData(Line):
    """ inlcude empty str """
    parts: list[str]

    def __bool__(self) -> bool:
        return bool(self.parts)


class Parser(ABC):
    """ SmalllConfig Parser """

    @property
    @abstractmethod
    def lineno(self) -> int:
        """ base 1 """
        pass

    @abstractmethod
    def _advance(self) -> str | None:
        pass

    @abstractmethod
    def _lookahead(self) -> str | None:
        """ return next line without moving cursor """
        pass

    def advance(self) -> str | None:
        self._cachedln = None
        next_line = self._advance()

        if next_line is not None:
            return next_line.strip()

        # else reach end

    def lookahead(self) -> str | None:
        """ witch cache """

        if self._cachedln is not None:
            return self._cachedln

        next_line = self._lookahead()

        if next_line is not None:
            self._cachedln = next_line.strip()
            return self._cachedln

    @property
    def shim_lineno(self) -> str:
        return f"[Ln: {self.lineno:2}]"

    def __init__(self, strict: bool, sep: str):
        self.strict = strict
        self.sep = sep
        self._cachedln = None

    def parse(self) -> SmallConfigData:
        # ulize python insert order dict
        sections = {  }

        while self.lookahead() is not None:
            section = self.parse_section()

            if section.name in sections and self.strict:
                raise SemanticsError(
                    f"duplicated section name {section.name}"
                )

            if section and section.name == SEC_SEP:
                if sections and self.strict:
                    raise SyntaxError(
                        f"place [{SEC_SEP}] at file top"
                    )

                self.sep = self.parse_sep(section.data[0][0])

            sections[section.name] = section

        if not sections and self.strict:
            raise RuntimeWarning('empty file')

        return SmallConfigData(
            sections=sections,
            sep = self.sep
        )

    def parse_section(self) -> Section:
        name: SectionName = self.parse_line(self.advance())

        if not isinstance(name, SectionName):
            raise SyntaxError(
                f"{self.shim_lineno} expect a section found {name}"
            )

        data = self.parse_section_data()

        return Section(name.name, data)

    def parse_section_data(self) -> list[list[str]]:
        """ parse strdata until next section or end """

        data = []

        while self.lookahead() is not None:
            # skip empty lines
            if not self.lookahead():
                self.advance()
                continue

            ln = self.parse_line(self.lookahead())

            if not isinstance(ln, StrData):
                break

            ln: StrData
            data.append(ln.parts)
            self.advance()

        return data

    def parse_line(self, ln: str) -> Line:
        # assert ln is not empty

        try:
            match ln[0]:
                case Bracket.LEFT:
                    return self.parse_section_name(ln)
                case _:
                    return self.parse_strdata(ln)
        except ValueError as ex:
            ex.add_note(self.shim_lineno)
            raise

    def parse_section_name(self, ln: str) -> SectionName:
        if len(ln) < 2 or ln[-1] != Bracket.RIGHT:
            raise SyntaxError(
                f"{self.shim_lineno} bad syntax on `{ln}`"
            )

        return SectionName(ln[1:-1].strip())

    def parse_strdata(self, ln: str) -> StrData:
        parts = []

        for seg in ESCAPE_RULE.split(ln, self.sep):
            seg = seg.strip()

            # trim white characters
            if not seg:
                continue

            parts.append(ESCAPE_RULE.unescape(seg))

        return StrData(parts)

    def parse_sep(self, ln: str) -> str:
        """ %{unicodepointin decimal} """

        m = re.match(r'%(\d+)', ln)

        if not m:
            raise SyntaxError(
                f"{self.shim_lineno} bad syntax after [{SEC_SEP}]"
            )

        return chr(int(m.groups()[0]))


class StrParser(Parser):

    @singledispatchmethod
    def __init__(self, rawinput, **kwargs):
        pass

    @__init__.register(list)
    def _(self, rawinput: list[str], **kwargs) -> None:
        super().__init__(**kwargs)

        # line index
        self.i = 0
        self.rawlines = rawinput

        # total lines
        self.end = len(self.rawlines)

    @__init__.register
    def _(self, rawinput: str) -> None:
        self.__init__(rawinput.splitlines())

    @property
    def lineno(self) -> int:
        return self.i + 1

    def _advance(self) -> str | None:
        self.i += 1

        if self.i < self.end:
            return self.rawlines[self.i]

    def _lookahead(self) -> str | None:
        if self.i + 1 < self.end:
            return self.rawlines[self.i + 1]


class StreamParser(Parser):
    @singledispatchmethod
    def __init__(self, rawinput, **kwargs):
        pass

    @__init__.register
    def _(self, rawinput: TextIOBase, **kwargs) -> None:
        super().__init__(**kwargs)

        self.stream = rawinput
        self.iter = peekable(self.stream)
        self.i = 0

    @property
    def lineno(self) -> int:
        return self.i + 1

    def _advance(self) -> str | None:
        self.i += 1

        return next(self.iter, None)

    def _lookahead(self) -> str | None:
        # tee bug https://github.com/python/cpython/issues/123884

        return self.iter.peek(None)


class Unparser:
    def __init__(
        self,
        data: SmallConfigData,
        fw: IOBase,
        strict: bool = True
    ):
        self.sections = data.sections
        self.sep = data.sep
        self.strict = strict
        self.fw = fw

        if not self.sections and self.strict:
            raise RuntimeWarning('empty content')

    def unparse(self) -> int:
        linesep = os.linesep
        sep = self.sep
        cnt = 0

        specialchars = SPECIALCHARS

        if sep not in SPECIALCHARS:
            specialchars += sep

        for name, section in self.sections.items():
            if name != section.name and self.strict:
                raise RuntimeWarning(
                    f"conflict key name {name}"
                    f" with real name {section.name}"
                )

            cnt += self.fw.write(
                f"{Bracket.LEFT}{ESCAPE_RULE.escape(specialchars, name)}"
                f"{Bracket.RIGHT}{linesep}"
            )

            for ln in section.data:
                rawparts = []

                for seg in ln:
                    rawparts.append(ESCAPE_RULE.escape(specialchars, seg))

                rawline = sep.join(rawparts)

                cnt += self.fw.write(
                    f"{rawline}{linesep}"
                )

        return cnt
