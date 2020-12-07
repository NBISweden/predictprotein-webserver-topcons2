#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from libpredweb import myfunc
from libpredweb import webserver_common as webcom

rundir = os.path.dirname(__file__)
basedir = os.path.realpath("%s/../"%(rundir))

progname=os.path.basename(sys.argv[0])
general_usage = """
usage: %s TESTMODE options
"""%(sys.argv[0])

numArgv = len(sys.argv)
if numArgv <= 1:
    print(general_usage)
    sys.exit(1)
TESTMODE=sys.argv[1]



if 0:#{{{
    infile = sys.argv[1]
    li = myfunc.ReadIDList2(infile, 2, None)
    print(li)
#}}}
if 0:#{{{
   rawseq = ">1\nseqAAAAAAAAAAAAAAAAAAAAAAAAA\n    \n>2  dad\ndfasdf  "
   #rawseq = "  >1\nskdfaskldgasdk\nf\ndadfa\n\n\nadsad   \n"
   #rawseq = ">sadjfasdkjfsalkdfsadfjasdfk"
   rawseq = "asdkfjasdg asdkfasdf\n"
   seqRecordList = []
   myfunc.ReadFastaFromBuffer(rawseq, seqRecordList, True, 0, 0)

   print(seqRecordList)
#}}}

if 0:#{{{
    size = float(sys.argv[1])
    print("size=",size)
    print("humansize=", myfunc.Size_byte2human(size))#}}}

if 0:#{{{
    newsfile = "%s/static/doc/news.txt"%(basedir)
    newsList = myfunc.ReadNews(newsfile)
    print(newsList)#}}}

if 0:#{{{
    seqfile="/data3/tmp/t3.seq"
    desp = "new description"
    webcom.ReplaceDescriptionSingleFastaFile(seqfile, desp)#}}}


if TESTMODE in ['writehtmltopcons']:#{{{
    try: 
        infile = sys.argv[2]
        outfile = sys.argv[3]
    except IndexError:
        print("usage: %s %s finished_seq outfile"%(sys.argv[0], TESTMODE))
        sys.exit(1)

    webcom.WriteHTMLResultTable_TOPCONS(outfile, infile)
    #}}}

if TESTMODE in ['sendmail']:#{{{
    try: 
        to_email = sys.argv[2]
        from_email = "noreply-TOPCONS@topcons.cbr.su.se"
        subject = "Result from TOPCONS2"
        bodytext = """This is the result from topcons2.
        The result can be found at https://topcons.net/result

        --
        Citation: 
        Please cite this paper if you find TOPCONS useful in your research
        The TOPCONS web server for combined membrane protein topology and signal peptide prediction.
        Tsirigos KD*, Peters C*, Shu N*, Käll L and Elofsson A (2015) Nucleic Acids Research 43 (Webserver issue), W401-W407.
        """

    except IndexError:
        print("usage: %s %s to_email"%(sys.argv[0], TESTMODE))
        sys.exit(1)

    myfunc.Sendmail(from_email, to_email, subject, bodytext)

    
