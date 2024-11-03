# -*- coding:utf-8 -*-

"""PwdKeeper
a small password keeper, query or add username-password by interactive shell

(*)   l list
(?)   q query
(+)   a add
(-)   d del
(^)   u update
(=>)    cd
(!)     sync
(??)  h help
(EOF) exit


Usage:
  pwd_keeper <path> [--username=<username>]

Options:
  <path>                      account file path to connect
  -u --username=<username>    your account name for pwd_keeper, using for check account file
"""


from contextlib import contextmanager, redirect_stdout
from io import StringIO
from math import inf
import re

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from functools import cache, partial
import getpass
from pathlib import Path
from threading import RLock
from typing import Any, Self
from string import whitespace

from prompt_toolkit import (
    PromptSession,
    print_formatted_text as print,
)
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.completion import (
    Completer,
    Completion,
    CompleteEvent,
)
from prompt_toolkit.validation import (
    Validator,
    ValidationError
)
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import (
    KeyBindings,
    KeyPressEvent,
    KeyPress
)
from prompt_toolkit.auto_suggest import (
    AutoSuggest,
    Suggestion
)
from prompt_toolkit.buffer import Buffer
import pyperclip

import minghu6
from docopt import docopt
from minghu6.cmd import askyesno
from minghu6.data import duplicated
from minghu6.etc.smallconfig import Section, SmallConfig, RW
from minghu6.functools import chain_apply, map, filter
from minghu6.metaclass import singleton, singleton_exit,  singleton_key
from minghu6.operators import get
from minghu6.security.des import des
from minghu6.string import split_blankline, split_whitespace
from minghu6.typing import StrPath


################################################################################
#### PwdKeeper Data

@dataclass
class Account:
    name: str
    pwd: str

    @classmethod
    def from_line(cls, ln: list[str]) -> Self:
        return cls(ln[0], ln[1])

    def into_line(self) -> list[str]:
        return [self.name, self.pwd]


LABEL_NAME_PATTERN = r'[a-zA-Z0-9%][a-zA-Z0-9_\.%]*'


@dataclass
class Label:
    name: str
    data: list[Account]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable[Account]:
        return iter(self.data)

    def account(self, name: str) -> Account | None:
        res = chain_apply(
            list,
            filter(lambda x: x.name == name),
            self.data
        )

        if res:
            return res[0]

    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.match(LABEL_NAME_PATTERN, name))

    @classmethod
    def from_section(cls, section: Section) -> Self:
        name = section.name
        data = [Account.from_line(ln) for ln in section.data]

        return cls(name, data)

    def into_section(self) -> Section:
        name = self.name
        data = [account.into_line() for account in self.data]

        return Section(name, data)


class RADMode(Enum):
    R = 'r'
    RA = 'ra'
    D = 'd'


R = RADMode.R
RA = RADMode.RA
D = RADMode.D


################################################################################
#### PwdKeeper Abstract

class PwdKeeperBase(ABC):

    @singleton_key
    @staticmethod
    def _normalize_path(path: StrPath, *_, **kw) -> Path:
        return Path(path)

    def __init__(
        self,
        path: StrPath,
        master_password: str,
        username: str | None = None,
    ):
        self._init_succeed = False

        self.path = self._normalize_path(path)
        self.config = SmallConfig(path, RW)
        self.validate_data(self.config)

        self.username = get(
            self.config,
            (r'%username', 0, 0),
            ''
        )

        if username is not None and self.username != username:
            raise ValueError(
                f"expect user: {username} found {self.username}"
            )

        self.master_password = master_password

        self.map_data()

        self.__post_init__()

        self._init_succeed = True

    def __post_init__(self):
        pass

    @abstractmethod
    def validate_data(self):
        pass

    @abstractmethod
    def map_data(self):
        pass

    @abstractmethod
    def reflect_data(self):
        pass

    def sync(self) -> int:
        self.reflect_data()
        return self.config.sync()

    @abstractmethod
    def unchecked_label(
        self,
        name: str,
        mode: RADMode = R,
        label: Label = None
    ) -> Label | None:
        """ Unchecked Operation """

        pass

    @abstractmethod
    def labels(self) -> Iterable[Label]:
        """ get all user labels """
        pass

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, pwd: str) -> str:
        pass

    @singleton_exit
    def exit(self):
        if self._init_succeed:
            self.sync()


################################################################################
#### PwdKeeper Behaviour

@singleton
class PwdKeeper(PwdKeeperBase):
    """ Data Model
    ```
    [label]
    + account, passwd
    ```
    """

    def __post_init__(self):
        self.master_password = des.valid_key(self.master_password)

    def encrypt(self, plaintext: str) -> str:
        return des.encryp_str(
            plaintext, self.master_password
        )

    def decrypt(self, pwd: str) -> str:
        return des.decryp_str(
            pwd, self.master_password
        )

    def validate_data(self, config: SmallConfig):
        for section in config.sections():
            if re.match(r'%.*', section.name):
                continue

            for ln in section.data:
                if len(ln) != 2 or not ln[0] or not ln[1]:
                    raise ValueError(
                        f"malformed data {ln} on [{section.name}]"
                    )

            dup = chain_apply(
                duplicated,
                map(lambda ln: ln[0]),
                section.data
            )

            if dup:
                raise ValueError(f"found dup items {dup}")

    def map_data(self):
        # build data map

        labels: dict[str, Label] = {}

        for section in self.config.sections():
            if re.match(r'%.*', section.name):
                continue

            label = Label.from_section(section)

            labels[label.name] = label

        self._labels = labels

    def reflect_data(self):
        for name, label in self._labels.items():
            section = label.into_section()

            if section.name in self.config:
                self.config[name] = section
            else:
                self.config.append(section)

        deleted = []

        for section in self.config.sections():
            if section.name not in self._labels:
                deleted.append(section.name)

        for name in deleted:
            self.config.pop(name)

    def unchecked_label(
        self,
        name: str,
        mode: RADMode = R,
    ) -> Label | None:
        match mode:
            case RADMode.R:
                return self._labels.get(name, None)

            case RADMode.RA:
                if name not in self._labels:
                    self._labels[name] = Label(name, [])

                return self._labels[name]

            case RADMode.D:
                return self._labels.pop(name)

    def labels(self) -> Iterable[Label]:
        return self._labels.values()


################################################################################
#### Command Data

HELPDOC = '\n'.join(split_blankline(__doc__)[:2])


class ActionError(ValueError, ABC):
    @property
    @abstractmethod
    def subject(self) -> str:
        pass

    @property
    @abstractmethod
    def reason(self) -> str:
        pass

    def __init__(self, *args: object) -> None:
        if args:
            name = args[0]
        else:
            name = ''

        super().__init__(f"{self.subject}: {name} {self.reason}")


class ExistsError(ActionError):
    @property
    def reason(self) -> str:
        return '<exist>'


class NotFoundError(ActionError):
    @property
    def reason(self) -> str:
        return ''


class SubjectAction(ActionError):
    @property
    def subject(self) -> str:
        return 'action'


class SubjectLabel(ActionError):
    @property
    def subject(self) -> str:
        return 'label'


class SubjectAccount(ActionError):
    @property
    def subject(self) -> str:
        return 'account'


class SubjectPasswd(ActionError):
    @property
    def subject(self) -> str:
        return 'passwd'


class SubjectPath(ActionError):
    @property
    def subject(self) -> str:
        return 'path'


class ActionNotFoundError(NotFoundError, SubjectAction):
    pass


class LabelExistsError(ExistsError, SubjectLabel):
    pass


class LabelNotFoundError(NotFoundError, SubjectLabel):
    pass


class AccountExistsError(ExistsError, SubjectAccount):
    pass


class AccountNotFoundError(ExistsError, SubjectAccount):
    pass


class PasswdExistsError(ExistsError, SubjectPasswd):
    pass


class PathNotFoundError(NotFoundError, SubjectPath):
    pass


class CDPath(StrEnum):
    PREV = r'(\.\.)[/]?$'
    NEXT = fr'({LABEL_NAME_PATTERN})'
    ANOTHER = fr'\.\./{NEXT}'

    @classmethod
    def parse(cls, path: str) -> tuple[Self, str | None]:
        for enumval in cls:
            m = re.match(enumval, path)

            if m:
                return (enumval, m.group())

        raise PathNotFoundError(path)


################################################################################
#### Command Abstract

class Command(Enum):
    L    = ('*', 'l', 'list')
    Q    = ('?', 'q', 'query')
    A    = ('+', 'a', 'add')
    D    = ('-', 'd', 'del')
    U    = ('^', 'u', 'update')
    CD   = ('=>', 'cd')
    SYNC = ('!', 'sync')
    H    = ('??', 'h', 'help')
    EXIT = ('exit', )


class ActionContext(ABC):
    """
    uncouple model based methods and output behaviour
    """

    @dataclass
    class InitData:
        db: PwdKeeper
        session: PromptSession
        shimstack: list[str] = field(default_factory=list)

        def copy(self) -> Self:
            return self.__copy__()

        def __copy__(self) -> Self:
            return ActionContext.InitData(
                db=self.db,
                session=self.session,
                shimstack=self.shimstack.copy()
            )

    def __init__(self, initdata: InitData) -> None:
        # unpackage manually for type hint

        self.initdata = initdata
        self.dbcli = initdata.db
        self.session = initdata.session
        self.shimstack = initdata.shimstack
        self._dryrun = False

    @property
    def shim(self) -> str:
        pshims = ' => '.join(self.shimstack)

        if pshims:
            pshims += ' => '

        shim = self._shim()

        return f"{pshims}{shim} ||"

    def enable_dryrun(self):
        with RLock():
            self._dryrun = True

    def disable_dryrun(self):
        with RLock():
            self._dryrun = False

    @contextmanager
    def dryrun(self):
        self.enable_dryrun()

        try:
            yield

        finally:
            self.disable_dryrun()

    @staticmethod
    def actions_to_complete() -> Iterable[str]:
        def _():
            yield from ActionContext.__abstractmethods__
            yield from ['??', 'help', 'sync', 'exit']

        return chain_apply(
            filter(lambda name: name not in 'plist',),
                map(lambda name: name[:-1]
                   if name.endswith('_') else name),
                _()
            )

    def dispatch(
        self,
        action_name: str
    ) -> Callable[..., Any]:
        method_name = None

        for cmd in Command:
            if action_name in cmd.value:
                method_name = cmd.value[-1]
                break

        if method_name is None:
            raise ActionNotFoundError(action_name)

        if hasattr(self, method_name):
            method = getattr(self, method_name)
        else:
            method = getattr(self, f"{method_name}_")

        return method

    def help(self, *args):
        if self._dryrun:
            return

        print(HELPDOC)

    def sync(self):
        if self._dryrun:
            return

        cnt = self.dbcli.sync()
        print(f'{cnt} bytes synchronized.')

    def exit(self):
        if self._dryrun:
            return

        clear()

    @abstractmethod
    def _shim(self) -> str:
        pass

    @abstractmethod
    def plist(self) -> Iterable[str]:
        pass

    @abstractmethod
    def list_(self):
        pass

    @abstractmethod
    def query(self, name: str):
        pass

    @abstractmethod
    def add(self, *_):
        pass

    @abstractmethod
    def del_(self, name: str):
        """ return old """
        pass

    @abstractmethod
    def update(self, *_):
        """ return old """
        pass

    @abstractmethod
    def cd(self, path) -> Self:
        pass


################################################################################
#### Command Implementations

class RootContext(ActionContext):

    def _shim(self) -> str:
        return self.dbcli.username

    def plist(self) -> Iterable[str]:
        for label in self.dbcli.labels():
            yield label.name

    def list_(self):
        if self._dryrun:
            return

        for i, name in enumerate(self.plist(), start=1):
            print(f"[{name}] ", end='')

            if i % 4 == 0:
                print()

    def query(self, name: str):
        label = self.dbcli.unchecked_label(name)

        if label is None:
            raise LabelNotFoundError(name)

        if self._dryrun:
            return

        for account in label.data:
            print(account.name)

        if not label:
            print('<Empty>')

        print()

    def add(self, name: str):
        if self._dryrun:
            label = self.dbcli.unchecked_label(name, R)

            if label:
                raise LabelExistsError(name)

            return

        label = self.dbcli.unchecked_label(name, RA)

        # for label is not None and not empty
        if label:
            raise LabelExistsError(name)

        print(f"label {name} added.")

    def del_(self, name: str):
        oldlabel = self.dbcli.unchecked_label(name)

        if oldlabel is None:
            raise LabelNotFoundError(name)

        if self._dryrun:
            return

        if oldlabel:
            stringbuffer = StringIO()

            with redirect_stdout(stringbuffer):
                print(f"[{name}]")

                for account in oldlabel.data:
                    account_name = account.name
                    plain_passwd = self.dbcli.decrypt(account.pwd)

                    print(f'{account_name}: {plain_passwd}')

            if not askyesno(f"{stringbuffer.getvalue()}", default=False):
                return

        oldlabel = self.dbcli.unchecked_label(name, D)

        print(f"label {oldlabel.name} removed.")

    def update(self, oldname: str, newname: str):
        oldlabel = self.dbcli.unchecked_label(oldname)

        if oldlabel is None:
            raise LabelNotFoundError(newname)

        if oldname == newname:
            raise LabelExistsError(oldname)

        if self._dryrun:
            return

        self.dbcli.unchecked_label(oldname, D)
        newlabel = self.dbcli.unchecked_label(newname, RA)

        newlabel.data = oldlabel.data

        print(f"label {oldname} renamed to {newname}.")

    def cd(self, path: str) -> ActionContext:
        pathenum, value = CDPath.parse(path)

        match pathenum:
            case CDPath.NEXT:
                label = self.dbcli.unchecked_label(value)

                if label is None:
                    raise PathNotFoundError(
                        f"path: {path}"
                    )

                initdata = self.initdata.copy()
                initdata.shimstack.append(self._shim())

                return LabelContext(
                    initdata,
                    label
                )

            case CDPath.ANOTHER:
                raise PathNotFoundError(
                    f"path: {path}"
                )

            case CDPath.PREV:
                return self


class LabelContext(ActionContext):
    def __init__(
        self,
        initdata: ActionContext.InitData,
        label: Label
    ):
        super().__init__(initdata)
        self.label = label

    def _shim(self) -> str:
        return self.label.name

    def plist(self) -> Iterable[str]:
        for account in self.label.data:
            yield account.name

    def list_(self):
        if self._dryrun:
            return

        for name in self.plist():
            print(name)

    def query(self, name: str) -> Account:
        account = self.label.account(name)

        if account is None:
            raise AccountNotFoundError(name)

        if self._dryrun:
            return

        plain_passwd = self.dbcli.decrypt(account.pwd)

        self.session.clipboard.set_data(plain_passwd)
        pyperclip.copy(plain_passwd)

        print(f"{plain_passwd} (copied)")

    def add(self, name: str, plain_passwd: str):
        if self.label.account(name):
            raise AccountExistsError(name)

        if self._dryrun:
            return

        self.label.data.append(Account(
            name,
            self.dbcli.encrypt(plain_passwd)
        ))

        print(f"account {name} added.")

    def del_(self, name: str):
        account = self.label.account(name)

        if not account:
            raise AccountNotFoundError(name)

        if self._dryrun:
            return

        self.label.data.remove(account)

        print(f"account {account.name} removed.")

    def update(self, name: str, plain_passwd: str):
        account = self.label.account(name)

        if not account:
            raise AccountNotFoundError(name)

        pwd = self.dbcli.encrypt(plain_passwd)

        if account.pwd == pwd:
            raise PasswdExistsError(plain_passwd)

        if self._dryrun:
            return

        account.pwd = pwd

        print(f"{account.name} password changed.")

    def cd(self, path: str) -> ActionContext:
        pathenum, value = CDPath.parse(path)

        match pathenum:
            case CDPath.NEXT:
                raise PathNotFoundError(
                    f"path: {path}"
                )

            case CDPath.ANOTHER:
                label = self.query(value)

                if label is None:
                    raise PathNotFoundError(
                        f"path: {path}"
                    )

                initdata = self.initdata.copy()

                return LabelContext(initdata, label)

            case CDPath.PREV:
                initdata = self.initdata.copy()
                initdata.shimstack.pop()

                return RootContext(initdata)


################################################################################
#### Interactive Shell Components

def split_words(text: str) -> list[str]:
    return split_whitespace(text)


def count_essential_params(f: Callable) -> int:
    """
    from https://stackoverflow.com/questions/57885922/\
count-positional-arguments-in-function-signature
    """

    tot = f.__code__.co_argcount

    if f.__defaults__ is not None:
        cnt_kw = len(f.__defaults__)
    else:
        cnt_kw = 0

    return tot - cnt_kw


def count_max_params(f: Callable) -> int:
    tot = f.__code__.co_argcount

    return tot


def complete_prefix(
    prefix: str,
) -> Callable[[Iterable[str]], Iterable[Completion]]:

    return partial(
        chain_apply,
        map(lambda name: Completion(name + '', -len(prefix))),
        filter(
            lambda name: name.startswith(prefix)
        ),
    )


def damerau_lavenstein_distance(w1: str, w2: str) -> int:
    @cache
    def solve(w1: str, w2: str) -> int:
        if len(w1) > len(w2):
            w1, w2 = w2, w1

        if not w1:
            return len(w2)

        if not w2:
            return 0

        l1 = len(w1)

        # case-1
        # insert a char

        case1 = 1 + solve(w1, w2[1:])

        # case-2
        # remove a char

        case2 = 1 + solve(w1[1:], w2)

        # case-3
        # replace a char

        if w1[0] == w2[0]:
            case3 = 0 + solve(w1[1:], w2[1:])
        else:
            case4 = 1 + solve(w1[1:], w2[1:])

        # case-4
        # swap with neighborhood char

        if l1 >= 2 and w1[:2][::-1] == w2[:2]:
            case4 = 2 + solve(w1[2:], w2[2:])
        else:
            case4 = inf

        return min(case1, case2, case3, case4)

    return solve(w1, w2)


class IntegrationCompleter(Completer):
    def __init__(self, ctx: ActionContext) -> None:
        super().__init__()

        self.ctx = ctx

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:

        words = split_words(document.text_before_cursor)

        argcnt = len(words)

        word_prefix = document.get_word_before_cursor()

        complete = complete_prefix(word_prefix)

        if word_prefix:
            argcnt -= 1

        if argcnt == 0 and complete_event.completion_requested:
            yield from complete(self.ctx.actions_to_complete())
            return

        if argcnt == 1:
            if (
                words[0]
                in Command.Q.value
                + Command.D.value
                + Command.U.value
                + Command.CD.value
            ):
                yield from complete(self.ctx.plist())

                return


class IntegrationValidator(Validator):
    def __init__(self, ctx: ActionContext) -> None:
        self.ctx = ctx

    def validate(self, document: Document) -> None:
        words = split_words(document.text)

        argcnt = len(words)

        if argcnt:
            argcnt += 1

        if argcnt >= 1:
            try:
                method = self.ctx.dispatch(words[0])
            except NotFoundError as ex:
                raise ValidationError(
                    message=ex.args[0],
                    cursor_position=0
                ) from ex

        if argcnt >= 2:
            expected_min = count_essential_params(method) - 1
            expected_max = count_max_params(method) - 1
            actual = len(words[1:])

            if actual < expected_min:
                raise ValidationError(
                    message=f"lack {expected_min - actual} parameter(s)",
                    cursor_position=0
                )

            if actual > expected_max:
                raise ValidationError(
                    message=f"exceed {actual - expected_max} parameter(s)",
                    cursor_position=0
                )

            with self.ctx.dryrun():
                try:
                    method(*words[1:])
                except ActionError as ex:
                    raise ValidationError(
                        message=ex.args[0],
                        cursor_position=0
                    ) from ex


class IntegrationSuggest(AutoSuggest):
    def get_suggestion(
        self, buffer: Buffer, document: Document
    ) -> Suggestion | None:

        offset = len(document.current_line_before_cursor)

        words = split_words(document.text)

        if len(words) == 1 and document.char_before_cursor == '=':
            return Suggestion("> ")


################################################################################
#### Interactive Shell Main Loop

def main(path, username=None):
    pwd = ''
    pwd = getpass.getpass("Input your master password: ")

    dbcli = PwdKeeper(path, pwd, username)


    kb = KeyBindings()

    session = PromptSession(
        key_bindings=kb,
    )

    ctx = RootContext(ActionContext.InitData(dbcli, session))

    ctx.help()

    while True:
        try:
            input_result: str | None = session.prompt(
                f"{ctx.shim} ",
                completer=IntegrationCompleter(ctx),
                validator=IntegrationValidator(ctx),
                auto_suggest=IntegrationSuggest()
            ).strip() # STRIP !!
        except EOFError:
            ctx.exit()
            break
        except KeyboardInterrupt:
            print('\n^Interrupt')
            break

        action_name, *args = split_words(input_result)

        action = ctx.dispatch(action_name)

        match action:
            case a if a == ctx.exit:
                ctx.exit(*args)
                break
            case a if a == ctx.cd:
                ctx = ctx.cd(*args)
            case _:
                action(*args)


################################################################################
#### CLI

def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    path = arguments["<path>"]

    main(
        path,
        username=arguments["--username"],
    )


if __name__ == "__main__":
    cli()
