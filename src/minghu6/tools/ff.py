# -*- coding:utf-8 -*-

"""ff
A ffmpeg wrapper
Usage:
  ff show     <filename> [--raw] [-d]
  ff pconvert [<filename>...] --format=<format> [-d] [--dry-run]
  ff protate  <filename>  --degree=<degree> [--output=<output>] [-d] [--dry-run]
  ff rotate   <filename> --transpose=<transpose>... [--output=<output>] [-d] [--dry-run]
  ff cut   (video | audio) <filename> <start-time> <end-time> [--output=<output>] [-d] [--dry-run]
  ff merge (video | audio) [<filename>...] [--pattern=<pattern>]... [--prefix=<prefix>]...
                           --output=<output> [-d] [--dry-run]
  ff merge video audio    <videoname> <audioname> --output=<output> [-d] [--dry-run]
  ff merge video subtitle <videoname> <subtitlename> --output=<output> [-d] [--dry-run]
  ff merge gif            [<filename>...] [--pattern=<pattern>]... [--prefix=<prefix>]...
                          --output=<output> [--framerate=<framerate>] [-d] [--dry-run]
  ff merge slide          [<filename>...] [--pattern=<pattern>]... [--prefix=<prefix>]...
                          --output=<output> [--secs=<secs>] [--music=<music>]
                          [--crf=<crf>] [-d] [--dry-run]
  ff extract video    <filename> --output=<output> [-d] [--dry-run]
  ff extract audio    <filename> --output=<output> [-d] [--dry-run]
  ff extract subtitle <filename> --output=<output> [-d] [--dry-run]
  ff extract frame    <filename> <start-time> --output=<output> [-d] [--dry-run]
  ff recompile [<filename>...] [--cv=<cv>] [--ca=<ca>] [-d] [--dry-run]
  ff vol [<filename>...] --factor=<factor> [-d] [--dry-run] [--output=<output>]

Options:
  info                       view the info of the file.
  pconvert                   pure convert without recompile codec
  protate                    pure (set video rotation metadata)
  rotate                     (counterclock with decimal integer degree)
  vol                        manufacturing volume of the video (recompile audio loseless)
  <start-time>               video start time, 0 means 00:00:00
  <end-time>                 video end time, [HH:]MM:SS[.m...], support placeholder `end` means for video end
  <title-type>               title type

     --raw                   print raw json
  -f --format=<format>       to format such as `mp4`
  -o --output=<output>       ouput file
  -l                         list all information
  -d --debug                 enable debug mode
  --transpose=<transpose>    (cclock_flip | clock | cclock | clock_flip) transpose
  --degree=<degree>          degree (decimal int)
  --dry-run                  dry run
  --prefix=<prefix>          file name prefix within the given directory,
                             e.g. `sub/img` matches names in `sub/`
  --pattern=<pattern>        regex pattern of file name within the given
                             directory, e.g. `sub/.*\\.png`
  --crf=<crf>                compressed output video quality from 0-51 [default: 16]
  --cv=<cv>                  video codec optional: [libx264 | libx265], [default: libx265].
  --ca=<ca>                  audio codec [default: aac]
    --factor=<factor>        {float number} x times volumn, 0.8, 1.5, etc...
    --framerate=<framerate>  {float number} [default: 25].
    --secs=<secs>            {float number} seconds for each slide [default: 5].
    --music=<music>          background music file, looped till the video ends.
"""


from abc import ABC, abstractmethod
from collections import deque
import glob
from dataclasses import InitVar, astuple, dataclass, field
from enum import Enum, StrEnum, auto
from fractions import Fraction
from functools import partial
from itertools import zip_longest
import json
from pathlib import Path
import re
import html

from datetime import datetime, timedelta
from contextlib import ExitStack, contextmanager
from math import ceil
from textwrap import TextWrapper
from threading import RLock
from typing import Any, Self, Type

from docopt import docopt
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.formatted_text import to_formatted_text, HTML
from prompt_toolkit.styles import Style, merge_styles
from schema import Schema, And, Use, Or, Regex, Optional

from minghu6 import __version__
from minghu6.cmd import (
    ask_goon,
    wait_run,
    askoverride,
    mkstempfile,
    realtime_run,
)
from minghu6.etc.path2uuid import path2uuid_in, path2uuid_out
from minghu6.itertools import nest
from minghu6.etc.smallconfig import Section, SmallConfig, W

################################################################################
#### Contants

PRESET_SET = {
    "ultrafast",
    "superfast",
    "veryfast",
    "faster",
    "fast",
    "medium",
    "slow",
    "slower",
    "veryslow",
    "placebo",
}

SUMMARY_FILE = Path(".ff.summary.txt")


################################################################################
#### Global Variables

FILE_CACHE: dict[Path, Info] = {}

################################################################################
#### Data Classes

class FileNamePattern(Enum):
    GLOB = auto()
    REGEX = auto()
    PREFIX = auto()


class TransposeConstant(Enum):
    CCLOCK_FLIP = 0
    CLOCK = 1
    CCLOCK = 2
    CLOCK_FLIP = 3

    @staticmethod
    def from_str(value: str) -> Self:
        return TransposeConstant[value.upper()]

    def __str__(self) -> str:
        return self.name.lower()


class CodecType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    DATA = "data"
    SUBTITLE = "subtitle"


class VideoCodec(StrEnum):
    """encoder name"""

    H264 = "libx264"
    H265 = "libx265"
    FAKE_PNG = "png"
    VP9 = "libvpx-vp9"
    AV1 = "libsvtav1"

    @classmethod
    def from_codec_name(cls, codec_name: str) -> Self:
        match codec_name:
            case "h264":
                return cls.H264
            case "hevc":
                return cls.H265
            case "vp9":
                return cls.VP9
            case "png":
                return cls.FAKE_PNG
            case "av1":
                return cls.AV1
            case _:
                raise ValueError(codec_name)


class AudioCodec(StrEnum):
    """encoder name"""

    AAC = "aac"
    LIBFDK_AAC = "libfdk_aac"
    FLAC = "flac"
    MP3 = "mp3"
    LIBMP3LAME = "libmp3lame"
    # Dolby Digital
    AC3 = "ac3"
    OPUS = "opus"
    LIBOPUS = "libopus"

    @classmethod
    def from_codec_name(cls, codec_name: str) -> Self:
        match codec_name:
            case "aac":
                return cls.AAC
            case "libfdk_aac":
                return cls.LIBFDK_AAC
            case "flac":
                return cls.FLAC
            case "mp3":
                return cls.MP3
            case "libmp3lame":
                return cls.LIBMP3LAME
            case "ac3":
                return cls.AC3
            case "opus":
                return cls.OPUS
            case "libopus":
                return cls.LIBOPUS
            case _:
                raise ValueError(codec_name)


class DataCodec(StrEnum):
    BIN = "bin_data"
    TIMED_ID3 = "timed_id3"


class SubtitleCodec(StrEnum):
    SRT = "srt"
    ASS = "ass"
    MOV_TEXT = "mov_text"


class H264VideoCodingProfile(Enum):
    """[`profile`](https://en.wikipedia.org/wiki/Advanced_Video_Coding#Profiles)"""

    BASE = "Base"
    CONSTRAINED_BASELINE = "Constrained Baseline"
    EXTENDED = "Extended"
    MAIN = "Main"
    MAIN10 = "Main 10"
    HIGHT = "High"
    HIGH10 = "High 10"
    # UNKNOWN = "Unknown"

class VP9VideoCodingProfile(Enum):
    PROFILE0 = "Profile 0"
    PROFILE1 = "Profile 1"
    PROFILE2 = "Profile 2"
    PROFILE3 = "Profile 3"

# # enum memebers iter on defined order
# class VideoCodingLevel(Enum):
#     """ a [`level`](https://en.wikipedia.org/wiki/Advanced_Video_Coding#Levels)
#     is a specified set of constraints that indicate
#     a degree of required decoder performance for a profile.
#     """

#     L1  = '1'
#     # L1B = '1b'
#     L11 = '1.1'
#     L12 = '1.2'
#     L13 = '1.3'
#     L2  = '2'
#     L21 = '2.1'
#     L22 = '2.2'
#     L3  = '3'
#     L31 = '3.1'
#     L32 = '3.2'
#     L4  = '4'
#     L41 = '4.1'
#     L42 = '4.2'
#     L5  = '5'
#     L51 = '5.1'
#     L52 = '5.2'
#     L6  = '6'
#     L61 = '6.1'
#     L62 = '6.2'

#     @classmethod
#     def from_int(cls, value: int) -> Self:
#         """
#         [store mapping](https://stackoverflow.com/questions/69983131/whats-the-difference-between-ffprobe-level-and-h-264-level)
#         """
#         for lv in cls:
#             if int(float(lv.value) * 30) == value:
#                 return lv

#         raise ValueError(f'{value} is not a valid {Self.__name__}')

RawCodingLevel = int


@dataclass
class AspectRatio:
    w: int
    h: int

    @classmethod
    def from_str(cls, s: str, sep=":") -> Self:
        w, h = s.split(sep)

        return cls(int(w), int(h))

    def __repr__(self) -> str:
        return f"{self.w}:{self.h}"


class SideDataType(Enum):
    DISPLAY_MATRIX = "Display Matrix"


@dataclass
class SideDataItemDisplay:
    rotation: int
    side_data_type: InitVar[SideDataType]


class UserTimeDelta(timedelta):

    @classmethod
    def from_secs(cls, secs: float | str) -> Self:
        return cls(seconds=float(secs))

    def as_hour_str(self) -> str:
        """
        hh:mm:ss.ms
        """

        tot_secs = self.total_seconds()

        tot_mins = tot_secs // 60
        tot_hs = tot_mins // 60

        return (
            f"{int(tot_hs):02}:{int(tot_mins % 60):02}:{round((tot_secs % 60), 2)}"
        )

    @classmethod
    def from_hour_str(cls, s: str) -> Self:
        """hh:mm:ss.ms"""

        secs = 0

        enumrator = enumerate(reversed(s.split(":")))

        i, t = next(enumrator)
        secs += float(t)

        for i, t in enumrator:
            secs += int(t) * 60**i

        return cls.from_secs(secs)


################################################################################
#### Context Managers


@contextmanager
def handle_inplace_output(fn: Path, output: Path | None):
    inplace = False

    if output is None:
        inplace = True
        suffix = str(datetime.now())
        suffix = re.sub(r"[\-|:]", "", suffix)
        suffix = re.sub(r"[ |.]", "_", suffix)

        output = fn.with_stem(f"{fn.stem}_{suffix}")

    try:
        yield output

    finally:
        if inplace and not DRY_RUN and output.exists():
            fn.unlink()
            output.rename(fn)


################################################################################
#### Validators

def expand_file_pattern(
    patterns: list[str], mode: FileNamePattern
) -> list[Path]:
    """
    Expand input patterns into existing file paths.

    - `GLOB`: literal existing file paths are collected directly, patterns
      with glob magic (`*`, `?`, `[`, `**`) expand by `glob.glob` where
      `**` means recursion, e.g. `'**/*.png'` or `'sub/*.png'`.
    - `REGEX`/`PREFIX`: the directory part of a pattern (e.g. `a/b/img`)
      locates the directory to look into, then the
      basename part of the pattern matches file names within that directory.
    """

    picked: list[Path] = []

    for pat in patterns:
        pat = Path(pat)

        match mode:
            case FileNamePattern.GLOB:
                if pat.is_file():
                    picked.append(pat)
                else:
                    for file in glob.iglob(pat, recursive=True):
                        file = Path(file)

                        if file.is_file():
                            picked.append(file)

            case FileNamePattern.REGEX | FileNamePattern.PREFIX:
                for file in pat.parent.iterdir():
                    if not file.is_file():
                        continue

                    if mode is FileNamePattern.REGEX:
                        matched = re.match(pat.name, file.name)
                    else:
                        matched = file.name.startswith(pat.name)

                    if matched:
                        picked.append(file)

    # remove duplicates and keep order
    return list(dict.fromkeys(picked))


################################################################################
#### Data Classes

class Loader(ABC):

    @classmethod
    @abstractmethod
    def load_dict(cls, d: dict[str, Any]) -> Self:
        pass


@dataclass
class VideoStream(Loader):
    codec_name: VideoCodec
    codec_type: InitVar[str]
    height: int
    width: int
    display_aspect_ratio: Fraction | None
    level: RawCodingLevel
    start_time: float
    # in seconds
    duration: UserTimeDelta
    profile: H264VideoCodingProfile | VP9VideoCodingProfile | None = None
    bit_rate: int | None = None
    side_data_list: InitVar[list[dict[str, Any]] | None] = None
    side_data: dict[SideDataType, SideDataItemDisplay] = field(
        default_factory=dict
    )

    def __post_init__(self, _codec_type, side_data_list):
        if side_data_list:
            for item in side_data_list:
                ty = item["side_data_type"]

                if ty is SideDataType.DISPLAY_MATRIX:
                    self.side_data[ty] = SideDataItemDisplay(**item)

    @classmethod
    def load_dict(cls: Type[Self], d: dict[str, Any]) -> Self:
        if "display_aspect_ratio" not in d:
            d["display_aspect_ratio"] = None

        return cls(**d)


@dataclass
class AudioStream(Loader):
    codec_name: AudioCodec
    codec_type: InitVar[str]
    duration: UserTimeDelta
    bit_rate: int | None = None

    @classmethod
    def load_dict(cls, d: dict[str, Any]) -> Self:
        return cls(**d)


@dataclass
class Info(Loader):
    filename: Path
    size: int
    tags: dict[str, Any]
    video: VideoStream | None = None
    audio: AudioStream | None = None

    @classmethod
    def load_dict(cls, d: dict[str, Any]) -> Self:
        d1 = {}

        d1["filename"] = d["format"]["filename"]
        d1["size"] = d["format"]["size"]
        d1["tags"] = d["format"].get("tags", {})

        for stream in d["streams"]:
            if stream["codec_type"] is CodecType.VIDEO:
                d1["video"] = VideoStream.load_dict(stream)
            if stream["codec_type"] is CodecType.AUDIO:
                d1["audio"] = AudioStream.load_dict(stream)

        return cls(**d1)


################################################################################
#### Schemas

SCHEMA_CLI = Schema(
    {
        "show": bool,
        "pconvert": bool,
        "protate": bool,
        "rotate": bool,
        "cut": bool,
        "merge": bool,
        "video": bool,
        "audio": bool,
        "gif": bool,
        "slide": bool,
        "extract": bool,
        "subtitle": bool,
        "frame": bool,
        "recompile": bool,
        "vol": bool,
        "--debug": bool,
        "--dry-run": bool,
        "<filename>": Use(
            partial(expand_file_pattern, mode=FileNamePattern.GLOB)
        ),
        "<videoname>": Or(None, And(Use(Path), lambda x: x.exists())),
        "<audioname>": Or(None, And(Use(Path), lambda x: x.exists())),
        "<subtitlename>": Or(
            None, And(Use(Path), lambda x: x.exists())
        ),
        "<start-time>": Or(
            None,
            And(
                Regex(r"^(\d+:){0,2}\d+(\.\d+)?"),
                Use(UserTimeDelta.from_hour_str),
            ),
        ),
        "<end-time>": Or(
            None,
            # lazy init to support special identifier `end`
            Regex(r"^(((\d+:){0,2}\d+(\.\d+)?)|end)"),
        ),
        "--raw": bool,
        "--degree": Or(None, And(Use(int), lambda n: 0 <= n <= 360)),
        "--transpose": [TransposeConstant.from_str],
        "--output": Or(None, And(Use(Path))),
        "--pattern": And(
            Use(
                partial(expand_file_pattern, mode=FileNamePattern.REGEX)
            ),
        ),
        "--prefix": And(
            Use(
                partial(
                    expand_file_pattern, mode=FileNamePattern.PREFIX
                )
            ),
        ),
        "--format": Or(
            None,
            Use(lambda ext: ext if ext.startswith(".") else "." + ext),
        ),
        "--cv": Or(None, Use(VideoCodec)),
        "--ca": Or(None, Use(AudioCodec)),
        "--factor": Or(None, Use(float)),
        "--framerate": Or(None, And(Use(float), lambda n: n > 0 and n <= 50.0)),
        "--secs": Or(None, And(Use(float), lambda n: n > 0)),
        "--music": Or(None, And(Use(Path), lambda p: p.exists())),
        "--crf": Or(None, And(Use(int), lambda n: 0 <= n <= 51)),
    },
)

SCHEME_SIEDE_DATA_LIST = Schema(
    [{"side_data_type": Use(SideDataType), Optional("rotation"): int}],
    ignore_extra_keys=True,
)

SCHEMA_VIDEO_STREAM = Schema(
    {
        "codec_name": Use(VideoCodec.from_codec_name),
        "codec_type": Use(CodecType),
        "width": int,
        "height": int,
        Optional("display_aspect_ratio"): Use(AspectRatio.from_str),
        Optional("profile"): Or(
            Use(H264VideoCodingProfile),
            Use(VP9VideoCodingProfile)
        ),
        "level": Use(RawCodingLevel),
        "start_time": Use(float),
        "duration": Use(UserTimeDelta.from_secs),
        Optional("bit_rate"): Use(int),
        Optional("side_data_list"): SCHEME_SIEDE_DATA_LIST,
    },
    ignore_extra_keys=True,
)

SCHEMA_AUDIO_STREAM = Schema(
    {
        "codec_name": Use(AudioCodec.from_codec_name),
        "codec_type": Use(CodecType),
        "duration": Use(UserTimeDelta.from_secs),
        Optional("bit_rate"): Use(int),
    },
    ignore_extra_keys=True,
)

SCHEMA_BIN_DATA_STREAM = Schema(
    { Optional("codec_name"): Use(DataCodec), "codec_type": Use(CodecType)},
    ignore_extra_keys=True,
)

SCHEMA_SUBTITLE_STREAM = Schema(
    {"codec_name": Use(SubtitleCodec), "codec_type": Use(CodecType)},
    ignore_extra_keys=True,
)

SCHEMA_STREAMS = Schema(
    [
        Optional(SCHEMA_VIDEO_STREAM),
        Optional(SCHEMA_AUDIO_STREAM),
        Optional(SCHEMA_BIN_DATA_STREAM),
        Optional(SCHEMA_SUBTITLE_STREAM)
    ],
    ignore_extra_keys=True,
)

SCHEMA_FORMAT = Schema(
    {
        "filename": Use(Path),
        "size": Use(int),
        Optional("tags"): {Optional("encoder"): str},
    },
    ignore_extra_keys=True,
)

SCHEMA_INFO = Schema(
    {"streams": SCHEMA_STREAMS, "format": SCHEMA_FORMAT},
    ignore_extra_keys=True,
)


################################################################################
#### Color Print Utils


class UbuntuColour(StrEnum):
    """

    :WARM_GREY: can be used for; backgrounds, graphics, dot patterns,
    charts and diagrams. It can also be used for large size text.
    """

    ORANGE = "E95420"
    WARM_GREY = "AEA79F"
    LIGHT_AUBERGINE = "77216F"
    MID_AUBERGINE = "5E2750"
    DARK_AUBERGINE = "2C001E"


CLS_ACTION = "action"
CLS_FILENAME = "filename"
CLS_SUCC = "succ"
CLS_WARN = "warn"
CLS_ERROR = "error"

DEFAULT_STYLE = Style.from_dict(
    {
        CLS_ACTION: f"bold",
        CLS_FILENAME: "italic",
        CLS_SUCC: "fg:#33D17A bold",
        CLS_WARN: "fg:#E9AD0C italic",
        CLS_ERROR: "fg:#C01C28 bold",
    }
)

# etc: gnome light
GNOME_LIGHT_STYLE = Style.from_dict(
    {
        CLS_ACTION: f"fg:#{UbuntuColour.ORANGE}",
        CLS_FILENAME: f"fg:#{UbuntuColour.WARM_GREY}",
    }
)

STYLE = merge_styles([DEFAULT_STYLE, GNOME_LIGHT_STYLE])


def style_print(*values, **kwargs):
    text = to_formatted_text(HTML("".join(values)))

    print_formatted_text(text, style=STYLE, **kwargs)


################################################################################
#### Global Configurations

DEBUG = False
DRY_RUN = False


@contextmanager
def tempory_set(**args):
    with RLock():
        nsbak = {}
        ns = globals()

        for k, v in args.items():
            nsbak[k] = ns[k]
            ns[k] = v

        try:
            yield
        finally:
            for k, v in nsbak.items():
                ns[k] = v


################################################################################
#### Main


class FF(ABC):
    def __init__(self, args: dict[str, Any]) -> None:
        self._args: dict[str, Any] = args
        self._schema: dict[str, Any] = SCHEMA_CLI.validate(args)

        self.input = self.collect_input()

        if not self.input:
            raise FileNotFoundError(f"_schema: {self._schema}")

        self._input = self.input
        self.output: Path | None = self._schema["--output"]

        if not DRY_RUN and self.output:
            if not self.output.stem:
                raise ValueError(
                    f"no explicit extension name for {self.output}"
                )

            if self.output.exists():
                if not askoverride(self.output, default=True):
                    exit()
                else:
                    self.output.unlink()

    def collect_input(self) -> list[Path]:
        # `<filename>`/`--pattern`/`--prefix` are all pre-expanded by
        # `expand_file_pattern` in the schema, which also keeps values
        # carrying a directory prefix (shell-expanded paths / quoted globs).
        return list(
            self._schema["<filename>"]
            + self._schema["--pattern"]
            + self._schema["--prefix"]
        )

    @staticmethod
    def exec_cmd(
        cmd: str, succ_msg: str | None = None, fetch=False
    ) -> str | int:
        """

        :return: if `fetch=False` then return retcode (int)
        else return fetched content (str)
        """

        # for consistent return type
        if DRY_RUN or DEBUG:
            print(f">>> Run: {cmd}")

            if DRY_RUN:
                if fetch:
                    return ""
                else:
                    return 0

        if fetch:
            res = wait_run(cmd)

            if not res.out:
                raise res.as_exception()

            if succ_msg is not None:
                style_print(succ_msg)

            return res.out

        else:
            retcode = realtime_run(cmd)

            if not retcode and succ_msg is not None:
                style_print(succ_msg)

            return retcode

    @abstractmethod
    def run(self):
        pass


class ListPrinter:

    #
    #   lwidth      rwidth
    # <----------||---------->

    class Line:
        pass

    @dataclass
    class Item(Line):
        key: str
        val: str

    @dataclass
    class Chapter(Line):
        name: str

    def __init__(
        self, lwidth: int = 15, rwidth: int = 20, ident: int = 4
    ) -> None:
        self.lines: list[ListPrinter.Item | ListPrinter.Chapter] = []
        self.lwidth = lwidth
        self.rwidth = rwidth
        self.ident = ident

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.execute()

    def pchapter(self, name):
        self.lines.append(ListPrinter.Chapter(str(name)))

    def pitem(self, key, value):
        self.lines.append(ListPrinter.Item(str(key), str(value)))

    def execute(self):
        ltext = TextWrapper(
            width=self.lwidth,
            initial_indent=" " * self.ident,
            subsequent_indent=" " * self.ident,
        )
        rtext = TextWrapper(width=self.rwidth)

        for ln in self.lines:
            match type(ln):
                case ListPrinter.Item:

                    llns = ltext.wrap(ln.key)
                    rlns = rtext.wrap(ln.val)

                    print(
                        f"{llns[0]:>{self.lwidth}} : {rlns[0]:<{self.rwidth}}"
                    )

                    for lln, rln in zip_longest(
                        llns[1:], rlns[1:], fillvalue=""
                    ):
                        print(
                            f"{lln:>{self.lwidth}}   {rln:<{self.rwidth}}"
                        )

                case ListPrinter.Chapter:

                    chlwidth = self.lwidth + ceil(len(ln.name) / 2) + 2
                    chtext = TextWrapper(width=chlwidth)
                    chs = chtext.wrap(f"[{ln.name}]")

                    print()
                    print()
                    for ch in chs:
                        print(f"{ch:>{chlwidth}}")
                    print()

        print()


class Show(FF):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.input = self.input[0]
        self.show_raw: bool = self._schema["--raw"]

    @staticmethod
    def _fetch_raw(fn_tmp: Path) -> dict:
        cmd = (
            f"ffprobe -v quiet -of json"
            f" -show_format -show_streams '{fn_tmp}'"
        )

        with tempory_set(DRY_RUN=False):
            out = FF.exec_cmd(cmd, fetch=True)

        return json.loads(out, strict=False)

    @staticmethod
    def fetch_info(fn_tmp: Path) -> Info:
        if fn_tmp not in FILE_CACHE:
            json = Show._fetch_raw(fn_tmp)
            obj = SCHEMA_INFO.validate(json)

            FILE_CACHE[fn_tmp] = Info.load_dict(obj)

        return FILE_CACHE[fn_tmp]

    def run(self):
        self.input: Path

        with path2uuid_in(self.input) as fn_tmp:
            from pprint import pprint

            if self.show_raw:
                pprint(self._fetch_raw(fn_tmp), sort_dicts=False)
                return

            info = self.fetch_info(fn_tmp)

            with ListPrinter() as ptr:
                ptr.pchapter("Main")

                ptr.pitem("filename", self.input.name)
                ptr.pitem("size", f"{info.size / (1024 * 1024):.1f} Mb")
                ptr.pitem("tags", info.tags)

                if info.video:
                    video = info.video

                    ptr.pchapter("Video")
                    ptr.pitem("codec_name", video.codec_name.value)
                    ptr.pitem(
                        "bit_rate",
                        (
                            f"{video.bit_rate / (1024 * 1024):.2f} Mb/s"
                            if video.bit_rate
                            else "unkonwn"
                        ),
                    )
                    ptr.pitem(
                        "resolution", f"{video.width} x {video.height}"
                    )
                    ptr.pitem("profile", video.profile.value if video.profile else "unkonwn")
                    ptr.pitem("level", video.level)
                    ptr.pitem("duration", video.duration.as_hour_str())

                if info.audio:
                    audio = info.audio

                    ptr.pchapter("Audio")
                    ptr.pitem("codec_name", audio.codec_name.value)
                    ptr.pitem("duration", audio.duration.as_hour_str())
                    ptr.pitem(
                        "bit_rate",
                        (
                            "unkonwn"
                            if audio.bit_rate is None
                            else f"{audio.bit_rate / (1024):.0f} Kb/s"
                        ),
                    )


class OneToOneAction(FF):
    @dataclass
    class Personality:
        cmd: str
        succ_msg: str

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.input: Path = self.input[0]

        if not self.input.stem:
            raise ValueError(
                f"no explicit extension name for {self.input}"
            )

    def run(self) -> int:

        with (
            handle_inplace_output(self.input, self.output) as output,
            path2uuid_in(self.input) as fn_tmp,
            path2uuid_out(output) as output_tmp,
        ):
            cmd: str
            cmd, succ_msg = astuple(
                self.personality(fn_tmp, output_tmp)
            )

            if DEBUG or DRY_RUN:
                str_in = str(self.input)
                str_out = str(output)

                width = max(len(str_in), len(str_out))

                print(f"     In: {str_in:>{width}} => {fn_tmp}")
                print(f"    Out: {str_out:>{width}} => {output_tmp}")

            if DRY_RUN:
                cmd = cmd.replace(str(fn_tmp), "[In]")
                cmd = cmd.replace(str(output_tmp), "[Out]")

            return self.exec_cmd(cmd, succ_msg=succ_msg)

    @abstractmethod
    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> Personality:
        pass


class OneToOneBatchAction(OneToOneAction):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.input: list[Path] = self._input

    @abstractmethod
    def parameters(self) -> dict[str, list[str]]:
        pass

    def run(self):
        if SUMMARY_FILE.exists() and not askoverride(SUMMARY_FILE):
            style_print("<error>Cancel.</error>")
            return

        config = SmallConfig(SUMMARY_FILE, W)

        key_todo = "todo"
        key_succ = "succ"
        key_fail = "failed"

        protected_keys = [key_todo, key_succ, key_fail]

        for k, v in self.parameters().items():
            if k in protected_keys:
                raise ValueError(f"override protected key `{k}`")

            config.append(Section(k, [v]))

        config.append(Section(key_todo, deque(nest(self.input))))
        config.append(Section(key_succ, []))
        config.append(Section(key_fail, []))

        todo: deque[list[Path]] = config[key_todo].data
        succ: list[Path] = config[key_succ].data
        faild: list[Path] = config[key_fail].data

        while todo:
            fn = todo.popleft()[0]

            self.input = fn
            retcode = super().run()

            if retcode:
                faild.append([fn])
                break

            succ.append([fn])


class OneToOneSameExt:
    """Mixin Class"""

    def check_ext(self: OneToOneAction) -> None:
        if self.output:
            if self.input.suffix != self.output.suffix:
                raise ValueError(
                    f"different ext name between"
                    f" {self.input} and {self.output}"
                )


class OneToOneDifferentExt:
    """Mixin Class"""

    def check_ext(self: OneToOneAction) -> None:
        if self.output:
            if self.input.suffix == self.output.suffix:
                raise ValueError(
                    f"same ext name between"
                    f" {self.input} and {self.output}"
                )


class ManyToOneAction(FF):
    @dataclass
    class Personality:
        cmd: str

    def run(self):
        input = sorted(self.input, key=lambda p: p.name)

        print("[Merge List]")

        for i, file in enumerate(input):
            print(f"{i:02d} {file.name}")

        if len(input) <= 1:
            print("Do nothing.")
            return

        if not DRY_RUN:
            if not ask_goon():
                return

        with ExitStack() as stack:
            input_tmp = [
                stack.enter_context(path2uuid_in(fn)) for fn in input
            ]
            output_tmp = stack.enter_context(path2uuid_out(self.output))
            mylist = stack.enter_context(mkstempfile(dir=Path.cwd()))

            with mylist.open("w") as fw:
                for fn in input_tmp:
                    fw.write(f"file {fn.name}\n")

            if DEBUG:
                print("[MYLIST.TXT]")

                with mylist.open() as f:
                    print(f.read())

            (cmd,) = astuple(self.personality(mylist, output_tmp))

            if DRY_RUN:
                cmd = cmd.replace(str(mylist), "[MYLIST.TXT]")

            self.exec_cmd(cmd, succ_msg="<succ>Done.</succ>")

    @abstractmethod
    def personality(
        self, mylist: Path, output_tmp: Path
    ) -> Personality:
        pass


class MergeVideo(ManyToOneAction):

    def personality(
        self, mylist: Path, output_tmp: Path
    ) -> ManyToOneAction.Personality:

        return super().Personality(
            f"ffmpeg -f concat -i {mylist} -c copy {output_tmp}"
        )


class MergeAudio(MergeVideo):
    pass


class MergeVideoAudio(ManyToOneAction):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.videoname = self._schema["<videoname>"]
        self.audioname = self._schema["<audioname>"]
        self.input = [self.videoname, self.audioname]

    def personality(
        self, mylist: Path, output_tmp: Path
    ) -> ManyToOneAction.Personality:

        return super().Personality(
            (
                f"ffmpeg -i {mylist}"
                f" -vcodec copy -acodec copy {output_tmp}"
            )
        )


class MergeVideoSubtitle(FF):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.subtitlename = self._schema["<subtitlename>"]
        self.input = self.input[0]

    def run(self):
        with (
            handle_inplace_output(self.input, self.output) as output,
            path2uuid_in(self.input) as fn_tmp,
            path2uuid_out(self.subtitlename) as subtitlename_tmp,
            path2uuid_out(self.output) as output_tmp,
        ):

            cmd = (
                f"ffmpeg -i {fn_tmp} -vf"
                f" subtitles='{subtitlename_tmp}' {output_tmp}"
            )

            succ_msg = (
                f"merge subtitle {html.escape(str(self.subtitlename))} into"
                f" {html.escape(str(self.input))}"
            )

            if self.output is not None:
                succ_msg += f" as {self.output}"

            if DEBUG or DRY_RUN:
                str_in0 = str(self.input)
                str_in1 = str(self.subtitlename)
                str_out = str(output)

                width = max(len(str_in0), len(str_in1), len(str_out))

                print(f"   In0: {str_in0:>{width}} => {fn_tmp}")
                print(
                    f"   In1: {str_in1:>{width}} => {subtitlename_tmp}"
                )
                print(f"   Out: {str_out:>{width}} => {output_tmp}")

            if DRY_RUN:
                cmd = cmd.replace(fn_tmp, "[In0]")
                cmd = cmd.replace(subtitlename_tmp, "[In1]")
                cmd = cmd.replace(output_tmp, "[Out]")

            else:
                with (
                    open(self.subtitlename, "rb") as fr,
                    open(subtitlename_tmp, "wb") as fw,
                ):
                    while chunk := fr.read(64 * 1024): fw.write(chunk)

            self.exec_cmd(cmd, succ_msg=succ_msg)


class MergeGif(ManyToOneAction):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.framerate: float = self._schema["--framerate"]

    def personality(
        self, mylist: Path, output_tmp: Path
    ) -> ManyToOneAction.Personality:

        return super().Personality(
            (
                f"ffmpeg -f image2 -framerate {self.framerate}"
                f" -i {mylist} {output_tmp}"
            )
        )


class MergeSlide(FF):
    """merge a set of photos into a slideshow video"""

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.secs: float = self._schema["--secs"]
        self.music: Path | None = self._schema["--music"]
        self.crf: int = self._schema["--crf"]

    @staticmethod
    def _probe_resolution(fn: Path) -> tuple[int, int]:
        cmd = (
            "ffprobe -v error -select_streams v:0"
            " -show_entries stream=width,height -of csv=p=0"
            f" '{fn}'"
        )

        with tempory_set(DRY_RUN=False):
            out = FF.exec_cmd(cmd, fetch=True)

        w, h = out.strip().split(",")

        return int(w), int(h)

    def run(self) -> int:
        input = sorted(self.input, key=lambda x: x.name)
        print("[Slide List]")

        for i, fn in enumerate(input):
            print(f"{i:02d} {fn.name} last {self.secs}s")

        size = self._probe_resolution(input[0])

        for fn in input[1:]:
            if self._probe_resolution(fn) != size:
                raise ValueError(
                    "photos must be of the same resolution:"
                    f" {input[0]} and {fn}"
                )

        with mkstempfile() as mylist, mylist.open("w") as fw:
            for fn in input:
                fw.write(f"file '{fn.resolve()}'\n")
                fw.write(f"duration {self.secs}\n")

            # duplicate last slide as sentinel
            # so the last slide lasts its full `secs`
            fw.write(f"file '{input[-1].resolve()}'\n")
            fw.flush()

            if DEBUG:
                print("[MYLIST.TXT]")
                with mylist.open() as f:
                    print(f.read())

            cmd = f"ffmpeg -f concat -safe 0 -i '{mylist}'"

            if self.music is not None:
                cmd += f" -stream_loop -1 -i '{self.music}'"

            cmd += (
                " -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2,setparams=range=pc'"
                " -bsf:v h264_metadata=video_full_range_flag=1"
                f" -c:v libx264 -crf {self.crf} -preset medium"
                " -pix_fmt yuv420p"
                " -g 1"  # each frame as keyframe
            )
            if self.music is not None:
                cmd += " -c:a aac -shortest"

            cmd += f" '{self.output}'"

            if DRY_RUN:
                cmd = cmd.replace(f"{mylist}", "[MYLIST.TXT]")

                if self.music is not None:
                    cmd = cmd.replace(f"'{self.music}'", "[MUSIC]")
            else:
                if not ask_goon():
                    return

            succ_msg = (
                f"<action>slide</action> {len(input)} photo"
                f"{'s' if len(input) > 1 else ''}"
                f" into <filename>{html.escape(str(self.output))}</filename>"
            )

            return self.exec_cmd(cmd, succ_msg=succ_msg)


class PRotate(OneToOneSameExt, OneToOneAction):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)
        self.check_ext()
        self.degree: int = self._schema["--degree"]

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:

        cmd = (
            f"ffmpeg -display_rotation {self.degree} -i {fn_tmp}"
            f" -codec copy {output_tmp}"
        )

        succ_msg = (
            f"rotate the video {html.escape(str(self.input))} "
            f"`{self.degree}`"
        )

        if self.output is not None:
            succ_msg += f" to {self.output}"

        return super().Personality(cmd, succ_msg)


class Rotate(OneToOneSameExt, OneToOneAction):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)
        self.check_ext()
        self.transpose: list[TransposeConstant] = self._schema[
            "--transpose"
        ]

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:

        vfargs = ",".join([f"transpose={t}" for t in self.transpose])

        cmd = f"ffmpeg -i {fn_tmp} -crf 17 -vf '{vfargs}' {output_tmp}"

        succ_msg = (
            f"<action>rotate</action> the video "
            f"<filename>{html.escape(str(self.input))}</filename> `{vfargs}`"
        )

        if self.output is not None:
            succ_msg += f" to <filename>{self.output}</filename>"

        return super().Personality(cmd, succ_msg)


class Cut(OneToOneSameExt, OneToOneAction):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)
        self.check_ext()
        self.start_time: UserTimeDelta = self._schema["<start-time>"]


class CutVideo(Cut):

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:
        info = Show.fetch_info(fn_tmp)

        if not info.video:
            raise ValueError(f"no video stream in {self.input}")

        if self._schema["<end-time>"] == "end":
            self.end_time = Show.fetch_info(fn_tmp).video.duration
        else:
            self.end_time = UserTimeDelta.from_hour_str(
                self._schema["<end-time>"]
            )

        duration = self.end_time - self.start_time

        if duration <= timedelta(0):
            raise ValueError(
                f"<end-time> {self.end_time.as_hour_str()}"
                f"should be greater than <start-time>"
                f"{self.start_time.as_hour_str()}"
            )

        cmd = (
            f"ffmpeg -ss {self.start_time.total_seconds()}"
            f" -i {fn_tmp} -t {duration.total_seconds()}"
            f" -c:v copy -c:a copy"
            f" -avoid_negative_ts auto {output_tmp}"
        )

        succ_msg = f"<action>Cut</action> as"

        if self.output is None:
            succ_msg += (
                f" <filename>{html.escape(str(self.input))}</filename>"
            )
        else:
            succ_msg += (
                f" <filename>{html.escape(str(self.output))}</filename>"
            )

        return super().Personality(cmd, succ_msg)


class CutAudio(Cut):

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:
        info = Show.fetch_info(fn_tmp)

        if not info.audio:
            raise ValueError(f"no audio stream in {self.input}")

        if self._schema["<end-time>"] == "end":
            self.end_time = Show.fetch_info(fn_tmp).audio.duration
        else:
            self.end_time = UserTimeDelta.from_hour_str(
                self._schema["<end-time>"]
            )

        duration = self.end_time - self.start_time

        if duration <= timedelta(0):
            raise ValueError(
                f"<end-time> {self.end_time.as_hour_str()}"
                f"should be greater than <start-time>"
                f"{self.start_time.as_hour_str()}"
            )

        cmd = (
            f"ffmpeg -ss {self.start_time.total_seconds()}"
            f" -i {fn_tmp} -t {duration.total_seconds()}"
            f" -c:v copy -c:a copy"
            f" -avoid_negative_ts auto {output_tmp}"
        )

        succ_msg = f"<action>Cut</action> as"

        if self.output is None:
            succ_msg += (
                f" <filename>{html.escape(str(self.input))}</filename>"
            )
        else:
            succ_msg += (
                f" <filename>{html.escape(str(self.output))}</filename>"
            )

        return super().Personality(cmd, succ_msg)


class PConvert(OneToOneDifferentExt, OneToOneAction):

    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)
        self.batch: list[Path] = self._input
        self.format = self._schema["--format"]

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:
        cmd = (
            f"ffmpeg -i {fn_tmp} -vcodec copy"
            f" -acodec copy {output_tmp}"
        )

        succ_msg = (
            f"<action>PConvert</action> to"
            f" <filename>{html.escape(str(self.output))}</filename> done."
        )

        return super().Personality(cmd, succ_msg)

    def run(self):
        for fn in self.batch:
            self.input = fn
            self.output = fn.with_suffix(self.format)
            self.check_ext()
            super().run()


class ReCompile(OneToOneBatchAction):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.ca = self._schema["--ca"]
        self.cv = self._schema["--cv"]

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:

        cmd = (
            f"ffmpeg -i {fn_tmp} -c:v {self.cv} -c:a {self.ca}"
            f" -crf 16 {output_tmp}"
        )

        succ_msg = (
            f"recompile {html.escape(str(self.input))} completed."
        )

        return OneToOneAction.Personality(cmd, succ_msg)

    def parameters(self) -> dict[str, list[str]]:
        return {"cv": [self.cv], "ca": [self.ca]}


class Vol(OneToOneBatchAction):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.factor: float = self._schema["--factor"]

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:
        self.input: Path

        cmd = (
            f"ffmpeg -i {fn_tmp} -filter:a 'volume={self.factor}'"
            f" -c:v copy {output_tmp}"
        )

        succ_msg = f"reset {html.escape(str(self.input))} volume {self.factor} times"

        return OneToOneAction.Personality(cmd, succ_msg)

    def parameters(self) -> dict[str, list[str]]:
        return {"factor": [str(self.factor)]}


class Extract(OneToOneAction):
    """Extract from (video) as something"""

    @property
    @abstractmethod
    def subcmd(self) -> str:
        pass

    def personality(
        self, fn_tmp: Path, output_tmp: Path
    ) -> OneToOneAction.Personality:

        cmd = f"ffmpeg -i {fn_tmp} {self.subcmd} {output_tmp}"
        succ_msg = (
            f"extract {html.escape(str(self.output))} "
            f"from {html.escape(str(self.input))} Done."
        )

        return OneToOneAction.Personality(cmd, succ_msg)


class ExtractVideo(Extract):
    @property
    def subcmd(self) -> str:
        return "-vcodec copy -an"


class ExtractAudio(Extract):
    @property
    def subcmd(self) -> str:
        return "-acodec copy -vn"


class ExtractSubtitle(Extract):
    @property
    def subcmd(self) -> str:
        return "-scodec copy -an -vn"


class ExtractFrame(Extract):
    def __init__(self, args: dict[str, Any]) -> None:
        super().__init__(args)

        self.start_time: UserTimeDelta = self._schema["<start-time>"]

    @property
    def subcmd(self) -> str:
        return (
            f"-y -f image2 -ss"
            f" {self.start_time.total_seconds()} -vframes 1"
        )


################################################################################
#### Docopt-Command Adapter


class FlatCommand(Enum):
    SHOW = Show
    PCONVERT = PConvert
    PROTATE = PRotate
    ROTATE = Rotate
    CUT_VIDEO = CutVideo
    CUT_AUDIO = CutAudio
    MERGE_VIDEO = MergeVideo
    MERGE_AUDIO = MergeAudio
    MERGE_VIDEO_AUDIO = MergeVideoAudio
    MERGE_VIDEO_SUBTITLE = MergeVideoSubtitle
    MERGE_GIF = MergeGif
    MERGE_SLIDE = MergeSlide
    EXTRACT_VIDEO = ExtractVideo
    EXTRACT_AUDIO = ExtractAudio
    EXTRACT_SUBTITLE = ExtractSubtitle
    EXTRACT_FRAME = ExtractFrame
    RECOMPILE = ReCompile
    VOL = Vol

    def as_cmd_list(self) -> list[str]:
        return list(map(lambda s: s.lower(), self.name.split("_")))

    @classmethod
    def derive_command(cls, args: dict[str, Any]) -> FF:
        for cmdenum in cls:
            if all(
                map(lambda substr: args[substr], cmdenum.as_cmd_list())
            ):
                return (cmdenum.value)(args)


def cli():
    args = docopt(__doc__, version=__version__)

    global DEBUG
    global DRY_RUN

    if args["--debug"]:
        DEBUG = True

    if args["--dry-run"]:
        DRY_RUN = True

    if DEBUG:
        with ListPrinter(lwidth=22, rwidth=50, ident=8) as ptr:
            ptr.pchapter("CLI Arguments")

            for k, v in args.items():
                ptr.pitem(k, v)

    return FlatCommand.derive_command(args).run()


if __name__ == "__main__":
    cli()
