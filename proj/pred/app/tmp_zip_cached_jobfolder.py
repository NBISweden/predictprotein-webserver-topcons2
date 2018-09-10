#!/usr/bin/env python

import sys
import os
import sqlite3
import argparse
import subprocess
import shutil

rundir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.realpath("%s/.."%(rundir)) # path of the application, i.e. pred/
path_result = "%s/static/result"%(basedir)
path_cache = "%s/static/result/cache"%(basedir)

if __name__ == '__main__':

#metavar='' is the text shown after then option argument
    parser = argparse.ArgumentParser(
            description='zip cached job folder',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''\
Created 2018-09-10, updated 2018-09-10, Nanjiang Shu

Examples:
    %s  -db dbname -exclude-md5 file
'''%(sys.argv[0]))
    parser.add_argument('-db' , metavar='DB', dest='db', required=True,
            help='the name of the finished date db')
    parser.add_argument('-exclude-md5' , metavar='FILE', dest='exclude_md5_file', required=True,
            help='name of the exclude md5 list file')

    args = parser.parse_args()

    db = args.db
    exclude_md5_file = args.exclude_md5_file

    exclude_md5_list = open(exclude_md5_file).read().split("\n")
    exclude_md5_set = set(exclude_md5_list)

    #print exclude_md5_set

    tbname_content = "data"

    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        cmd =  "SELECT md5, seq, date_finish FROM %s"%(tbname_content)
        cur.execute(cmd)
        rows = cur.fetchall()
        cnt = 0
        for row in rows:
            cnt += 1
            md5_key = row[0]
            seq = row[1]
            date_finish = row[2]
            if not md5_key in exclude_md5_set:
                subfoldername = md5_key[:2]
                md5_subfolder = "%s/%s"%(path_cache, subfoldername)
                cachedir = "%s/%s/%s"%(path_cache, subfoldername, md5_key)
                zipfile_cache = cachedir + ".zip"
                if os.path.exists(cachedir) and not os.path.exists(zipfile_cache):
                    origpath = os.getcwd()
                    os.chdir(md5_subfolder)
                    cmd = ["zip", "-rq", "%s.zip"%(md5_key), md5_key]
                    cmdline = " ".join(cmd)
                    try:
                        print("%d: %s"%(cnt, cmdline))
                        subprocess.check_call(cmd)
                        print("%d: %s"%(cnt, "rmtree(%s)"%(md5_key) ))
                        shutil.rmtree(md5_key)
                    except:
                        print >> sys.stderr, "Failed to zip folder %s"%(cachedir)
                        raise
                    os.chdir(origpath)

