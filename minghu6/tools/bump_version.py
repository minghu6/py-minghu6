"""
Inpired by cargo ws

LANG=en_US.UTF-8

1. repo uninit -> fatal exit
2. repo -> stage -> dirty -> commit select -> normal exit
                                           -> 3 -> commit with tag
                 -> clean -> no previous commit -> fatal exit
                                                -> 3
3 gettag -> has prev tag -> inc -> 4
                         ->  input new tag -> 4

4 git tag

"""

from typing import Optional, Callable, List, NamedTuple
from packaging.version import Version, InvalidVersion
from sys import stderr
import re

from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.auto_suggest import Suggestion, AutoSuggest
# from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.styles import Style


from simple_term_menu import TerminalMenu

from sh import git, ErrorReturnCode

init_version = 'v0.1.0'

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_>=]|\[[0-?]*[ -/]*[@-~])')

class Exit(Exception):
    pass


class RemoteConfigItem(NamedTuple):
    name: str
    url: str
    scope: str


class BoolValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text.lower()

        if not text:
            raise ValidationError(
                message='<Empty>',
                cursor_position=0
            )
        elif text and text not in ('y', 'yes', 'n', 'no'):
            raise ValidationError(
                message='Just input Yes or No',
                cursor_position=len(text)
            )


class TripleValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text.lower()

        if not text:
            raise ValidationError(
                message='<Empty>',
                cursor_position=0
            )
        elif text not in ('y', 'yes', 'n', 'no', 'a', 'all'):
            raise ValidationError(
                message='Just input All, Yes or No',
                cursor_position=len(text)
            )


class VersionValidator(Validator):
    def __init__(self, pre_version: Optional[Version] = None) -> None:
        super().__init__()
        self.pre_version = pre_version

    def validate(self, document: Document) -> None:
        text = document.text.lower()

        if not text:
            raise ValidationError(
                message='<Empty>',
                cursor_position=0
            )
        else:
            try:
                v = Version(text)
            except InvalidVersion:
                raise ValidationError(
                    message='Invalid version number',
                    cursor_position=len(text)
                )
            else:
                if self.pre_version is not None and v <= self.pre_version:
                    raise ValidationError(
                        message=f'No greater than {self.pre_version}',
                        cursor_position=len(text)
                    )


class RemoteValidator(Validator):
    def __init__(self, options: List[RemoteConfigItem]) -> None:
        super().__init__()
        self.options = options

    def validate(self, document: Document) -> None:
        text = document.text.lower()

        if not text:
            raise ValidationError(
                message='<Empty>',
                cursor_position=0
            )
        else:
            matched = False

            for e in self.options:
                if e.name.startswith(text) and len(e.name) >= len(text):
                    matched = True
                    break

            if not matched:
                raise ValidationError(
                    message=f'Non exist remote name',
                    cursor_position=len(text)
                )


class RemoteSuggest(AutoSuggest):
    def __init__(self, options: List[RemoteConfigItem]) -> None:
        super().__init__()
        self.options = options

    def get_suggestion(
        self, buffer: "Buffer", document: Document
    ) -> Optional[Suggestion]:
        text = document.text

        for e in self.options:
            if e.name.startswith(text) and len(e.name) >= len(text):
                return Suggestion(e.name[len(text):])

        return Suggestion('')


class InitVerSuggest(AutoSuggest):
    def get_suggestion(
        self, buffer: "Buffer", document: Document
    ) -> Optional[Suggestion]:
        if not document.current_line_before_cursor:
            return Suggestion(init_version)

        if 'v0.1.0'.startswith(document.current_line_before_cursor):
            return Suggestion(init_version[len(document.current_line_before_cursor):])
        else:
            return Suggestion('')

# TODO (maybe):
# check spec tag commit:  git rev-list -n 1 --abbrev-commit v1.4.5
# check latest tag commit: git rev-parse --short HEAD


def get_versions() -> List[Version]:
    # set tty_out False to forbid partially print
    raw = git('tag', _tty_out=False)

    if not raw:
        return

    versions = []

    for _, ln in enumerate(raw.strip().splitlines()):
        ln = ansi_escape.sub('', ln)

        if not ln:
            continue

        # print(i, ln.encode(), f"/{len(ln)}")

        try:
            v = Version(ln)
        except InvalidVersion as ex:
            pass
        else:
            versions.append(v)

    versions.sort()

    return versions


def get_remotes() -> List[RemoteConfigItem]:
    items = []

    for ln in git(['remote', '-v']).splitlines():
        ln = ansi_escape.sub('', ln)

        name, rem = ln.split('\t')
        url, scope = rem.split(' ')

        items.append(RemoteConfigItem(name, url, scope[1:-1]))

    return items


class App:
    """hook_version_inc:  如果暂存区是空的，需要修改文件后提交；否则修改文件后只是加入暂存区即可"""

    def __init__(self, hook_version_inc: Callable[[Version], None] = None ) -> None:
        self.hook_version_inc = hook_version_inc

    def run(self):
        try:
            version = self.commit_and_tag()
            self.push(version)
        except KeyboardInterrupt:
            print_formatted_text(FormattedText([
                ('skyblue', '^C '),
                ('pink', 'KeyboardInterrupt'),
            ]))
        except ErrorReturnCode as code:
                print_formatted_text(FormattedText([
                    ('red bold', '\u2718 '),
                    ('crimson', str(code)),
                ]), file=stderr)
        except Exit:  # just exit
            pass

    def push(self, version: Version):
        remotes = get_remotes()
        options = list(filter(lambda e: e.scope == 'push', remotes))

        if not remotes:
            print_formatted_text(FormattedText([
                ('moccasin bold', '\u26a0 '),
                ('gold', 'no configured remote repo (push)'),
            ]), file=stderr)

            return

        default_conf = None

        for e in options:
            if e.name == 'origin':
                default_conf = e
                break

        if default_conf is None:
            default_conf = remotes[0]

        labels = [
            ('lightgray bold', '\u21AA '),
            ('white bold', 'Push remote: '),
            ('', '['),
        ]

        match len(options):
            case 1:
                remote_select = [
                    ('firebrick', options[0].name)
                ]
            case 2:
                remote_select = [
                    ('firebrick', options[0].name),
                    ('', '|'),
                    ('khaki', options[1].name)
                ]
            case 3:
                remote_select = [
                    ('firebrick', options[0].name),
                    ('', '|'),
                    ('khaki', options[1].name),
                    ('', '|'),
                    ('seagreen', options[2].name),
                ]
            case 4:
                remote_select = [
                    ('firebrick', options[0].name),
                    ('', '|'),
                    ('khaki', options[1].name),
                    ('', '|'),
                    ('seagreen', options[2].name),
                    ('', '|'),
                    ('turquoise', options[3].name),
                ]
            case _:
                remote_select = ['', '|'.join(map(lambda e: e.name, options))]

        labels.extend(remote_select)
        labels.append(('', '] '))

        remote_name = prompt(FormattedText(labels),
            default=default_conf.name,
            validate_while_typing=True,
            validator=RemoteValidator(options),
            auto_suggest=RemoteSuggest(options),
            # completer=WordCompleter(list(map(lambda e: e.name, options)))
        )

        for e in options:
            if e.name == remote_name:
                seleced = e
                break

        try:
            git(['push', remote_name])
            git(['push', remote_name, f'v{version.public}'])
        except ErrorReturnCode as code:
            print(code.stderr.decode())
        else:
            print_formatted_text(FormattedText([
                ('skyblue bold', '\u2713 '),
                ('white bold', f'Push into {remote_name} ({seleced.url})'),
            ]))


    def commit_and_tag(self) -> Version:
        try:
            st = git('status', _tty_out=False)
        except ErrorReturnCode as code:
            if code.startswith('fatal: not a git repository'):
                print_formatted_text(FormattedText([
                    ('red bold', '\u2718 '),
                    ('crimson', 'not a git repository'),
                ]), file=stderr)
            elif code.stderr.startswith(b'nothing to commit'):
                pass
            else:
                print(code, file=stderr)

            raise Exit

        # staging area is clean
        if st.find('nothing to commit') != -1 or st.find('nothing added to commit') != -1:
            # no previous commit
            if st.find('No commits yet') != -1:
                print_formatted_text(FormattedText([
                    ('red bold', '\u2718 '),
                    ('crimson', 'no commits yet'),
                ]), file=stderr)

                raise Exit

            version = self.get_next_tag()
            if not self.confirm_create_version():
                raise Exit


            if callable(self.hook_version_inc):
                self.hook_version_inc(version)

        else:
            print(st)

            triple = prompt(FormattedText([
                ('lightgray bold', '\u21AA '),
                ('white bold', 'Commit confirmed '),
                ('', '['),
                ('khaki', 'a(ll)'),
                ('mediumpurple', '/y(es)/'),
                ('linen', 'n(o)'),
                ('', '] ')
            ]),
                default='a',
                validate_while_typing=True,
                validator=TripleValidator()
            )
            print()

            triple = triple.lower()

            if triple in ('n', 'no'):
                raise Exit

            version = self.get_next_tag()
            if not self.confirm_create_version():
                raise Exit

            if callable(self.hook_version_inc):
                self.hook_version_inc(version)

            if triple in ('a', 'all'):
                git(['commit', '-am', f'"tag v{version.public}"'])
            else:
                git(['commit', '-m', f'"tag v{version.public}"'])

        git(['tag', f'v{version.public}'])

        return version


    def confirm_create_version(self):
        res = prompt(FormattedText([
            ('lightgray bold', '\u21AA '),
            ('white bold', 'Create version confirmed? '),
            ('', '['),
            ('saddlebrown', 'y/'),
            ('linen', 'n'),
            ('', '] ')]
        ),
            default='y',
            validate_while_typing=True,
            validator=BoolValidator()
        )

        return res.lower() in ('y', 'yes')

    def get_next_tag(self) -> Optional[Version]:
        versions = get_versions()

        if not versions:
            # Key-in version

            print_formatted_text(FormattedText([
                ('skyblue', 'info '),
                ('pink', 'there is no (valid) tag'),
            ]))

            version_raw = prompt(FormattedText([
                ('lightgray bold', '\u21AA  '),
                ('white bold', 'Enter an initial version: '),
            ]),
                default=init_version,
                auto_suggest=InitVerSuggest(),
                validator=VersionValidator()
            )

            version = Version(version_raw)
        else:
            # Increase version

            pre_version = versions[-1]

            print_formatted_text(FormattedText([
                ('skyblue', 'info '),
                ('pink', 'current common version '),
                ('', str(pre_version))
            ]))

            m1 = pre_version.major
            m2 = pre_version.minor
            m3 = pre_version.micro
            pre = pre_version.pre

            major = Version(f'{m1+1}.{m2}.{m3}')
            minor = Version(f'{m1}.{m2+1}.{m3}')
            micro = Version(f'{m1}.{m2}.{m3+1}')

            options = [
                f' Patch ({micro.public})',
                f' Minor ({minor.public})',
                f' Major ({major.public})',
            ]

            pre_release = None
            pre_nxt = None

            if pre is not None and len(pre) == 2:
                pre_release = Version(f'{m1}.{m2}.{m3+1}-{pre[0]}{pre[1]+1}')
                options.append(f' Prerelease ({pre_release.public})')

                if pre[0] == 'a':
                    pre_nxt = Version(f'{m1}.{m2}.{m3+1}-beta0')
                    options.append(f' Beta ({pre_nxt.public})')

            options.append(f' Custom Version')

            terminal_menu = TerminalMenu(
                options,
                title="Select a new version:",
                menu_cursor='\u276f',
                menu_cursor_style=('fg_green', 'bold'),
                menu_highlight_style=('fg_cyan', ),
                raise_error_on_interrupt=True
            )

            nxt_ver_idx = None

            while nxt_ver_idx is None:
                nxt_ver_idx = terminal_menu.show()

            match nxt_ver_idx:
                case 0: version = micro
                case 1: version = minor
                case 2: version = major
                case _:
                    if options[nxt_ver_idx].find('Prerelease') != -1:
                        version = pre_release
                    elif options[nxt_ver_idx].find('Beta') != -1:
                        version = pre_nxt
                    elif options[nxt_ver_idx].find('Custom Version') != -1:
                        version_raw = prompt(FormattedText([
                            ('lightgray bold', '\u21AA  '),
                            ('white bold', 'Enter custom version: '),
                        ]),
                            validator=VersionValidator(pre_version)
                        )

                        version = Version(version_raw)

            print_formatted_text(FormattedText([
                ('skyblue bold', '\u2713 '),
                ('white bold', f'Select a new version: {version.public}'),
            ]))

        return version




if __name__ == '__main__':
    App().run()
