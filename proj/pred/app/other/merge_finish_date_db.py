#!/usr/bin/env python

import sys
import sqlite3
import argparse

if __name__ == '__main__':

#metavar='' is the text shown after then option argument
    parser = argparse.ArgumentParser(
            description='Merge sqlite3 database for TOPCONS2 cache finish date',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''\
2018-09-07

Examples:
    %s  -outdb log/merged.sqlite3 db1 db2 db3
'''%(sys.argv[0]))
    parser.add_argument('-outdb' , metavar='OUTDB', dest='outdb', required=True,
            help='the name of the database to be merged')
    parser.add_argument('dbnamelist', metavar='FILE', nargs='*',
            help='supply one or more dbs to be merged')

    args = parser.parse_args()

    outdb = args.outdb
    dbList = args.dbnamelist

    con3 = sqlite3.connect(outdb)

    tbname_content = "data"
    with con3:
        cur3 = con3.cursor()
        cur3.execute("""
            CREATE TABLE IF NOT EXISTS %s
            (
                md5 TEXT PRIMARY KEY,
                seq TEXT,
                date_finish TEXT
            )"""%(tbname_content))


        for db in dbList:
            con = sqlite3.connect(db)
            with con:
                cur = con.cursor()
                cmd =  "SELECT md5, seq, date_finish FROM %s"%(tbname_content)
                cur.execute(cmd)
                rows = cur.fetchall()
                for row in rows:
                    md5_key = row[0]
                    seq = row[1]
                    date_finish = row[2]
                    cmd =  "INSERT OR REPLACE INTO %s(md5,  seq, date_finish) VALUES('%s', '%s','%s')"%(tbname_content, md5_key, seq, date_finish)
                    cur3.execute(cmd)



