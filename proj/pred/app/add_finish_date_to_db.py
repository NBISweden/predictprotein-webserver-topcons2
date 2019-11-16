#!/usr/bin/python
# -*- coding: utf-8 -*-

# Description: Add the date of the job (when it is finished and saved in the
# cache) to the SQLite3 database

import os
import sys
import time
import argparse
import sqlite3

tbname_stat = "stat"
tbname_content = "data"
STEP_SHOW = 1000

def AddFinishDateToDB(path_cache, outdb):# {{{
    if not os.path.exists(path_cache):
        print("path_cache %s does not exist. Exit!", file=sys.stderr)
        return 1
    cntseq = 0
    con = sqlite3.connect(outdb)
    with con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS %s
            (
                md5 TEXT PRIMARY KEY,
                seq TEXT,
                date_finish TEXT
            )"""%(tbname_content))

        cnt_dir_level1 = 0
        cnt_dir_level2 = 0
        for dir1 in os.listdir(path_cache):
            path1 = os.path.join(path_cache, dir1)
            cnt_dir_level1 += 1
            for dir2 in os.listdir(path1):
                path2 = os.path.join(path1, dir2)
                if os.path.isdir(path2) and (len(dir2) == 32):
                    cnt_dir_level2 += 1

                    if cnt_dir_level2 % STEP_SHOW == 1:
                        print(("Processing #dir_level1 %4d, #dir_level2 %4d"%(cnt_dir_level1, cnt_dir_level2)))

                    md5_key = dir2
                    seq = ""
                    path2 = os.path.join(path1, dir2)
                    targetfile = os.path.join(path2, "query.result.txt")
                    seqfile = os.path.join(path2, "seq.fa")
                    if os.path.exists(targetfile):
                        seq = ""
                        if os.path.exists(seqfile):
                                content = open(seqfile,"r").read()
                                try:
                                    seq  = content.split("\n")[1]
                                except:
                                    pass
                        date_finish = time.strftime('%Y-%m-%d %H:%M:%S %Z', 
                            time.localtime(os.path.getmtime(targetfile)))
                        cmd =  "INSERT OR REPLACE INTO %s(md5,  seq, date_finish) VALUES('%s', '%s','%s')"%(tbname_content, md5_key, seq, date_finish)
                        cur.execute(cmd)

                    else:
                        try:
                            shutil.rmtree(path2)
                        except Exception as e:
                            print("Failed to delete broken result folder %s"%(path2), file=sys.stderr)



# }}}


if __name__ == '__main__':

#metavar='' is the text shown after then option argument
    parser = argparse.ArgumentParser(
            description='Add date of creation for jobs to the database',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''\
2018-02-23

Examples:
    %s -d result/cache -outdb log/cached_job_finished_date.sqlite3
'''%(sys.argv[0]))
    parser.add_argument('-d', metavar='PATH_CACHE', dest='path_cache', required=True,
            help='Provide path for the cached result')
    parser.add_argument('-outdb' , metavar='OUTDB', dest='outdb', required=True,
            help='the name of the database to be saved')
    parser.add_argument('-v', dest='verbose', nargs='?', type=int, default=0, const=1, 
            help='show verbose information, (default: 0)')

    args = parser.parse_args()

    path_cache = args.path_cache
    outdb = args.outdb
    verbose=args.verbose

#     print path_cache
#     print outdb

    rtvalue = AddFinishDateToDB(path_cache, outdb)
    sys.exit(rtvalue)

