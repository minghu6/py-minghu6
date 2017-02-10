# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os
import uuid
import sqlite3

from minghu6.io.stdio import askoverride
def path2uuid(i, d=False, include_ext=False, db=None, rename=True, quiet=False):
    """

    :param i:
    :param d:
    :param include_ext:
    :param db:
    :return: result_name in db
    """

    create_tb = ('\n'
                 '        CREATE TABLE IF NOT EXISTS Path2UUID\n'
                 '        (IBase VARCHAR UNIQUE,\n'
                 '         TmpBase VARCHAR UNIQUE\n'
                 '        );\n'
                 )

    if db is None:
        db = '.path2uuid.sqlite3'

    conn = sqlite3.connect(db)
    conn.execute(create_tb)
    cur = conn.cursor()

    i_base, ext = os.path.splitext(os.path.basename(i))
    if not d:

        if not include_ext:
            tmp_base = os.path.join(os.path.dirname(i),
                                    uuid.uuid3(uuid.NAMESPACE_DNS,
                                              os.path.basename(i_base)).hex)
        else:
            tmp_base = os.path.join(os.path.dirname(i),
                                    uuid.uuid3(uuid.NAMESPACE_DNS,
                                              os.path.basename(i)).hex)

        try:
            insert_sql = "INSERT INTO Path2UUID VALUES ('%s', '%s')"%(i_base, tmp_base)
            try:
                cur.execute(insert_sql)
            except sqlite3.IntegrityError:
                if quiet:
                    pass
                else:
                    raise

            if not include_ext: # CORE!!
                tmp_base += ext
            if rename:
                if askoverride(tmp_base, default=True):
                    os.remove(tmp_base)
                os.rename(i, tmp_base)
        except:
            conn.close()
            raise
        else:
            conn.commit()
            return tmp_base

    else:
        select_sql = """SELECT IBase FROM Path2UUID WHERE TmpBase='%s' """%i_base

        cur.execute(select_sql)
        res = cur.fetchone()
        if res is None:
            return

        res= res[0]
        try:
            output = res+ext
            if rename:
                if askoverride(output, default=True):
                    os.remove(output)
                os.rename(i, output)

            delete_sql = """DELETE FROM Path2UUID WHERE TmpBase='%s' """%i_base
            cur.execute(delete_sql)
        except:
            raise
        else:
            conn.commit()
            return res+ext
            #