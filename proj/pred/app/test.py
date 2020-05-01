#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import myfunc
import webserver_common as webcom

rundir = os.path.dirname(__file__)
basedir = os.path.realpath("%s/../"%(rundir))

progname=os.path.basename(sys.argv[0])
general_usage = """
usage: %s TESTMODE options
"""%(sys.argv[0])

numArgv = len(sys.argv)
if numArgv <= 1:
    print general_usage
    sys.exit(1)
TESTMODE=sys.argv[1]



if TESTMODE == "readidlist2":#{{{
    infile = sys.argv[2]
    li = myfunc.ReadIDList2(infile, 2, None)
    print li
#}}}
if TESTMODE == "readfastafrombuffer" :#{{{
   rawseq = ">1\nseqAAAAAAAAAAAAAAAAAAAAAAAAA\n    \n>2  dad\ndfasdf  "
   #rawseq = "  >1\nskdfaskldgasdk\nf\ndadfa\n\n\nadsad   \n"
   #rawseq = ">sadjfasdkjfsalkdfsadfjasdfk"
   rawseq = "asdkfjasdg asdkfasdf\n"
   seqRecordList = []
   myfunc.ReadFastaFromBuffer(rawseq, seqRecordList, True, 0, 0)

   print seqRecordList
#}}}

if TESTMODE == "byte2human":#{{{
    size = float(sys.argv[2])
    print "size=",size
    print "humansize=", myfunc.Size_byte2human(size)#}}}

if TESTMODE == "readnews":#{{{
    newsfile = "%s/static/doc/news.txt"%(basedir)
    newsList = myfunc.ReadNews(newsfile)
    print newsList#}}}

if TESTMODE == "replacedesp":#{{{
    seqfile="/data3/tmp/t3.seq"
    desp = "new description"
    webcom.ReplaceDescriptionSingleFastaFile(seqfile, desp)#}}}

if TESTMODE in ['writehtmltopcons']:#{{{
    try: 
        infile = sys.argv[2]
        outfile = sys.argv[3]
    except IndexError:
        print "usage: %s %s finished_seq outfile"%(sys.argv[0], TESTMODE)
        sys.exit(1)
    webcom.WriteHTMLResultTable_TOPCONS(outfile, infile) #}}}

if TESTMODE == "urlretrieve":
    url = sys.argv[2]
    outfile = sys.argv[3]
    timeout = int(sys.argv[4])
    try:
        myfunc.urlretrieve(url, outfile, timeout)
    except Exception as e:
        print("retrieve %s failed with errmsg=%s"%(url, str(e)) )

