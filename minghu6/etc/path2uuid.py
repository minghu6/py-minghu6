# -*- coding:utf-8 -*-

from contextlib import contextmanager
from pathlib import Path

import sqlite3
import uuid

from exports import export

from minghu6.cmd import askoverride
from minghu6.metaclass import singleton, singleton_exit, singleton_key
from minghu6.typing import *


@export
@contextmanager
def path2uuid_in(
    i: StrPath, dbpath: StrPath | None = None, rename_back: bool = True
):
    """
    :return: result_name in db
    """

    p = Path2UUID(dbpath=dbpath)
    uuidpath = None

    try:
        uuidpath = p.encode(i, rename=True)
        yield uuidpath
    finally:
        if uuidpath:
            p.decode(uuidpath, rename=rename_back)


@export
@contextmanager
def path2uuid_out(
    i: StrPath, dbpath: StrPath | None = None, rename_back: bool = True
):
    """
    :return: result_name in db
    """

    p = Path2UUID(dbpath=dbpath)
    uuidpath = None

    try:
        uuidpath = p.encode(i, rename=False)
        yield uuidpath
    finally:
        if uuidpath:
            p.decode(uuidpath, rename=rename_back)


@export
@singleton
class Path2UUID:
    @singleton_key
    @staticmethod
    def _normalize_dbpath(dbpath: StrPath | None = None) -> Path:
        if dbpath is None:
            dbpath = Path(".path2uuid.sqlite3")
        else:
            dbpath = Path(dbpath)

        return dbpath

    def __init__(self, dbpath: StrPath | None = None):
        dbpath = self._normalize_dbpath(dbpath)
        con = sqlite3.connect(dbpath)
        con.execute(
            (
                "\n"
                "CREATE TABLE IF NOT EXISTS Path2UUID\n"
                "        (I VARCHAR UNIQUE,\n"
                "         Tmp VARCHAR UNIQUE\n"
                "        );\n"
            )
        )

        self.con = con
        self.dbpath: Path = dbpath

    def _query_tmp(self, name: str) -> str | None:
        res = self.con.execute(
            "SELECT I FROM Path2UUID WHERE TMP=?", (name,)
        ).fetchone()

        if res is None:
            return

        return res[0]

    def encode(self, fpath: StrPath, rename=True) -> Path | None:
        """
        :return: rename failed return `None`
        """

        fpath = Path(fpath)
        tmppath = fpath.with_stem(
            uuid.uuid3(uuid.NAMESPACE_DNS, fpath.stem).hex
        )

        if self._query_tmp(tmppath.name) is None:
            # fail to roll back if insert multiple else commit
            with self.con:
                self.con.execute(
                    "INSERT INTO Path2UUID VALUES (?, ?)",
                    (fpath.name, tmppath.name),
                )

        if rename:
            if tmppath.exists():
                if askoverride(tmppath, default=True):
                    tmppath.unlink()
                else:
                    return

            if fpath.exists():
                fpath.rename(tmppath)

        return tmppath

    def decode(self, fpath: StrPath, rename=True) -> Path | None:
        fpath = Path(fpath)

        origin_name = self._query_tmp(fpath.name)

        if origin_name is None:
            return

        origin = Path(origin_name)

        if rename:
            if origin.exists():
                if askoverride(origin, default=True):
                    origin.unlink()
                else:
                    return

            if fpath.exists():
                fpath.rename(origin)

        with self.con:
            self.con.execute("DELETE FROM Path2UUID WHERE Tmp=?", (fpath.name,))

        return origin

    @singleton_exit
    def close(self):
        self.con.close()
