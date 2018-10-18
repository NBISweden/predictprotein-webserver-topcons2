#!/usr/bin/env python

import sys
import os
import sqlite3
import argparse
import subprocess
import shutil
import platform
from zipfile import ZipFile

rundir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.realpath("%s/.."%(rundir)) # path of the application, i.e. pred/
path_result = "%s/static/result"%(basedir)
path_cache = "%s/static/result/cache"%(basedir)

linux_dist = platform.dist()[0].lower()

user  = "www-data"
group = "www-data"
if linux_dist in ["centos", "redhat"]:
    user = "apache"
    group = "apache"
elif linux_dist in ["debian", "ubuntu"]:
    user = "www-data"
    group = "www-data"
else:
    print >> sys.stderr, "Unrecognized platform %s"%(linux_dist)
    sys.exit(1)

def ZipResultFolder(md5_key, cnt):
    """Zip the result folder
    """
    subfoldername = md5_key[:2]
    md5_subfolder = "%s/%s"%(path_cache, subfoldername)
    cachedir = "%s/%s/%s"%(path_cache, subfoldername, md5_key)
    zipfile_cache = cachedir + ".zip"
    if os.path.exists(cachedir) and not os.path.exists(zipfile_cache):
        origpath = os.getcwd()
        os.chdir(md5_subfolder)
        targetfile = os.path.join(cachedir, "query.result.txt")
        if os.path.exists(targetfile):
            cmd = ["zip", "-rq", "%s.zip"%(md5_key), md5_key]
            cmdline = " ".join(cmd)
            try:
                print("%d: %s"%(cnt, cmdline))
                subprocess.check_call(cmd)
                print("%d: %s"%(cnt, "rmtree(%s)"%(md5_key) ))
                os.system("chown %s:%s %s"%(user, group, "%s.zip"%(md5_key)))
                shutil.rmtree(md5_key)
            except:
                print >> sys.stderr, "Failed to zip folder %s"%(cachedir)
                raise
        else:
            print("%d: %s"%(cnt, "bad result! just rmtree(%s)"%(md5_key) ))
            shutil.rmtree(md5_key)
        os.chdir(origpath)
    elif os.path.exists(zipfile_cache):
        #check weather the zipped file is a valid prediction result
        try:
            with ZipFile(zipfile_cache, "r") as myzip:
                li = myzip.namelist()
                target = "%s/query.result.txt"%(md5_key)
                if target in li:
                    print("%d: %s"%(cnt, "Valid zipped result for %s"%(md5_key) ))
                else:
                    print("%d: %s"%(cnt, "bad zipped result! just delete zipfile(%s)"%(md5_key) ))
                    os.remove(zipfile_cache)
        except Exception as e:
            print("%d: %s"%(cnt, "BadZipFile! just delete zipfile(%s)"%(md5_key) ))
            os.remove(zipfile_cache)


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
    parser.add_argument('-db' , metavar='DB', dest='db', required=False,
            help='the name of the finished date db')
    parser.add_argument('-exclude-md5' , metavar='FILE', dest='exclude_md5_file', required=False,
            help='name of the exclude md5 list file')
    parser.add_argument('-md5' , metavar='FILE', dest='md5_file', required=False,
            help='name of the include md5 list file')

    args = parser.parse_args()

    db = args.db
    exclude_md5_file = args.exclude_md5_file
    md5_file = args.md5_file

    if not db == None:
        exclude_md5_list = open(exclude_md5_file).read().split("\n")
        exclude_md5_set = set(exclude_md5_list)
        #print exclude_md5_set
        tbname_content = "data"

        con = sqlite3.connect(db)
        with con:
            cur = con.cursor()
            cmd =  "SELECT md5, seq, date_finish FROM %s"%(tbname_content)
            cnt = 0
            for row in cur.execute(cmd):
#             print row
                cnt += 1
                md5_key = row[0]
                seq = row[1]
                date_finish = row[2]
                if not md5_key in exclude_md5_set:
                    ZipResultFolder(md5_key, cnt)
    elif not md5_file == None:
        md5_list = open(md5_file).read().split("\n")
        md5_list = filter(None, md5_list)
        cnt = 0
        for md5_key in md5_list:
            cnt += 1
            ZipResultFolder(md5_key, cnt)



