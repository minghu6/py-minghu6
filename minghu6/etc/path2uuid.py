# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""
import os
import sqlite3
import uuid

from minghu6.io.stdio import askoverride


def path2uuid(i, d=False, db=None, rename=True, quiet=False):
    """

    :param i:
    :param d:
    :param rename:
    :param db:
    :param quiet:
    :return: result_name in db
    """

    create_tb = ('\n'
                 '        CREATE TABLE IF NOT EXISTS Path2UUID\n'
                 '        (I VARCHAR UNIQUE,\n'
                 '         Tmp VARCHAR UNIQUE\n'
                 '        );\n'
                 )

    if db is None:
        db = '.path2uuid.sqlite3'

    conn = sqlite3.connect(db)
    conn.execute(create_tb)
    cur = conn.cursor()

    i_base, ext = os.path.splitext(os.path.basename(i))
    if not d:

        tmp_base = os.path.join(os.path.dirname(i),
                                uuid.uuid3(uuid.NAMESPACE_DNS,
                                           os.path.basename(i)).hex)

        tmp = tmp_base + ext
        try:
            insert_sql = "INSERT INTO Path2UUID VALUES ('%s', '%s')" % (i, tmp)
            try:
                cur.execute(insert_sql)
            except sqlite3.IntegrityError:
                if quiet:
                    pass
                else:
                    raise

            if rename:
                if askoverride(tmp, default=True):
                    os.remove(tmp)
                os.rename(i, tmp)
        except:
            conn.close()
            raise
        else:
            conn.commit()
            return tmp

    else:
        select_sql = """SELECT I FROM Path2UUID WHERE Tmp='%s' """ % i

        cur.execute(select_sql)
        res = cur.fetchone()
        if res is None:
            return

        res = res[0]
        try:
            output = res
            if rename:
                if askoverride(output, default=True):
                    os.remove(output)
                try:
                    os.rename(i, output)
                except:
                    if quiet:
                        pass
                    else:
                        raise

            delete_sql = """DELETE FROM Path2UUID WHERE Tmp='%s' """ % i
            cur.execute(delete_sql)
        except:
            raise
        else:
            conn.commit()
            return res
            #
