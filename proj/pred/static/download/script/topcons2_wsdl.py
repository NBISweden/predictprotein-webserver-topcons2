#!/usr/bin/env python

# Description: access topcons.net via WSDL service
# Copyright Nanjiang Shu (nanjiang.shu@scilifelab.se)

from __future__ import print_function
import os
import sys
import argparse
progname =  os.path.basename(sys.argv[0])
wspace = ''.join([" "]*len(progname))

no_suds_message="""\
suds is not installed!
Please install suds by

$ pip install suds  (for Python2)
$ pip install suds-jurko (for Python3)
"""

try:
    from suds.client import Client
except ImportError:
    print(no_suds_message, file=sys.stderr)
    sys.exit(1)

import urllib

MAX_FILESIZE_IN_MB = 9
MAX_FILESIZE = MAX_FILESIZE_IN_MB*1024*1024

def ReadFile(infile, mode="r"):#{{{
    try: 
        fpin = open(infile, mode)
        content = fpin.read()
        fpin.close()
        return content
    except IOError:
        print("Failed to read file %s with mode '%s'"%(infile, mode), file=sys.stderr)
        return ""
#}}}

def main(g_params):#{{{
    wsdl_url = "http://topcons.net/pred/api_submitseq/?wsdl"
    parser = argparse.ArgumentParser(
            description='Access topcons2 web-server (http://topcons.net) through WSDL service ',
            #formatter_class=argparse.RawDescriptionHelpFormatter,
            formatter_class=argparse.RawTextHelpFormatter,
            epilog='''\
Created 2015-02-04, updated 2018-01-12, Nanjiang Shu

Examples:
    # submit test.fa with jobname 'test' to the server 
    %s -m submit -seq test.fa -jobname test

    # try to retrieve the result for jobid 'rst_TTT' and save it to the current directory
    %s -m get -jobid rst_TTT
'''%(progname, progname))
    parser.add_argument('-m',  action='store',
        dest='mode', default='submit', choices=['submit','get'], required=True,
        help='Set the mode of API\nsubmit - submit a job to WSDL\nget    - retrieve the result from the server')
    parser.add_argument('-seq', metavar='FILE', dest='seqfile',
            help='Supply input sequence in FASTA format')
    parser.add_argument('-jobname', metavar='STR', dest='jobname',
            help='Give the job a name')
    parser.add_argument('-jobid', metavar='STR', dest='jobid',
            help='Retrieve the result by supplying a valid jobid')
    parser.add_argument('-email', metavar='STR', dest='email',
            help='Send a notification to the email when the result is ready')
    parser.add_argument('-outpath', metavar='DIR', dest='outpath',
            help='Save the retrieved data to outpath, (default: ./)')


    args = parser.parse_args()

    mode = args.mode

    jobid = ""
    email = ""
    jobname = ""
    fixtopfile = ""
    seqfile = ""
    outpath = "."

    if args.jobid != None:
        jobid = args.jobid
    if args.email != None:
        email = args.email
    if args.jobname != None:
        jobname = args.jobname
    if args.seqfile != None:
        seqfile = args.seqfile
    if args.outpath != None:
        outpath = args.outpath

    if mode == "submit":
        if seqfile == "":
            print("You want to submit a job but seqfile is not set. Exit!", file=sys.stderr)
            return 1
        elif not os.path.exists(seqfile):
            print("seqfile %s does not exist. Exit!"%(seqfile),file=sys.stderr)
            return 1

        try:
            filesize = os.path.getsize(seqfile)
        except OSError:
            print("failed to get the size of seqfile %s. Exit"%(seqfile), file=sys.stderr)
            return 1

        if filesize >= MAX_FILESIZE:
            print("You input seqfile %s exceeds the upper limit %d Mb."%(
                seqfile, MAX_FILESIZE_IN_MB), file=sys.stderr)
            print("Please split your seqfile and submit again.",  file=sys.stderr)
            return 1
        seq = ReadFile(seqfile)

        fixtop = ""
        if fixtopfile != "":
            fixtop = ReadFile(fixtopfile)
        myclient = Client(wsdl_url, cache=None)
        retValue = myclient.service.submitjob(seq, fixtop, jobname, email)
        if len(retValue) >= 1:
            strs = retValue[0]
            jobid = strs[0]
            result_url = strs[1]
            numseq_str = strs[2]
            errinfo = strs[3]
            warninfo = strs[4]
            if jobid != "None" and jobid != "":
                print("You have successfully submitted your job "\
                        "with %s sequences. jobid = %s\n"%(numseq_str, jobid))
                if warninfo != "" and warninfo != "None":
                    print("Warning message: %s\n"%str(warninfo))
            else:
                print("Failed to submit job!\n")
                if errinfo != "" and errinfo != "None":
                    print("Error message:%s\n"% str(errinfo))
                if warninfo != "" and warninfo != "None":
                    print("Warning message:%s\n"% str(warninfo))
        else:
            print("Failed to submit job!")
            return 1
    else:
        if jobid == "":
            print("You want to get the result of a job but jobid is not set. Exit!", file=sys.stderr )
            return 1
        myclient = Client(wsdl_url, cache=None)
        retValue = myclient.service.checkjob(jobid)
        if len(retValue) >= 1:
            strs = retValue[0]
            status = strs[0]
            result_url = strs[1]
            errinfo = strs[2]
            if status == "Failed":
                print("Your job with jobid %s is failed!"%(jobid))
                if errinfo != "" and errinfo != "None":
                    print("Error message:\n"%str(errinfo))
            elif status == "Finished":
                print("Your job with jobid %s is finished!"%(jobid))
                if not os.path.exists(outpath):
                    try:
                        os.makedirs(outpath)
                    except OSError:
                        print("Failed to create the outpath %s"%(outpath))
                        return 1
                outfile = "%s/%s.zip"%(outpath, jobid)
                urllib.urlretrieve (result_url, outfile)
                if os.path.exists(outfile):
                    print("The result file %s has been retrieved for jobid %s"%(outfile, jobid))
                else:
                    print("Failed to retrieve result for jobid %s"%(jobid))
            elif status == "None":
                print("Your job with jobid %s does not exist! Please check you typing!"%(jobid))
            else:
                print("Your job with jobid %s is not ready, status = %s"%(jobid, status))
        else:
            print("Failed to get job!")
            return 1

    return 0

#}}}

def InitGlobalParameter():#{{{
    g_params = {}
    g_params['isQuiet'] = True
    return g_params
#}}}
if __name__ == '__main__' :
    g_params = InitGlobalParameter()
    sys.exit(main(g_params))
