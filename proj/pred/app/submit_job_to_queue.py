#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: submit job to queue
import os
import sys
import subprocess
import time
import math
from libpredweb import myfunc
from libpredweb import webserver_common as webcom
import json
suq_exec = "/usr/bin/suq"
progname =  os.path.basename(__file__)
wspace = ''.join([" "]*len(progname))

rundir = os.path.dirname(os.path.realpath(__file__))
webserver_root = os.path.realpath("%s/../../../"%(rundir))
basedir = os.path.realpath("%s/.."%(rundir)) # path of the application, i.e. pred/
vip_email_file = "%s/config/vip_email.txt"%(basedir) 

rundir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.realpath("%s/../"%(rundir))
python_exec = "python"
suq_basedir = "/tmp"
gen_errfile = "%s/static/log/%s.log"%(basedir, progname)

usage_short="""
Usage: %s -nseq INT -jobid STR -outpath DIR -datapath DIR
       %s -email EMAIL -host IP -baseurl BASE_WWW_URL
       %s -nseq-this-user INT
       %s -only-get-cache [-force]

Description: 
    BASE_WWW_URL e.g. topcons.net
"""%(progname, wspace, wspace, wspace)

usage_ext="""
Description:
    Submit job to queue
    datapath should include query.fa

OPTIONS:
  -only-get-cache   Only get the cached results, this will be run on the front-end
  -force            Do not use cahced result
  -nseq-this-user   Number of sequences in the queue submitted by this user
  -h, --help    Print this help message and exit

Created 2015-01-20, updated 2019-11-20, Nanjiang Shu
"""
usage_exp="""
Examples:
    %s -jobid rst_mXLDGD -outpath /data3/result/rst_mXLDGD -datapath /data3/tmp/tmp_dkgSD
"""%(progname)

def PrintHelp(fpout=sys.stdout):#{{{
    print(usage_short, file=fpout)
    print(usage_ext, file=fpout)
    print(usage_exp, file=fpout)#}}}

def SubmitJobToQueue(jobid, datapath, outpath, numseq, numseq_this_user, email, #{{{
        host_ip, base_www_url):
    webcom.loginfo("Entering SubmitJobToQueue()", g_params['debugfile'])
    fafile = "%s/query.fa"%(datapath)
    query_parafile = "%s/query.para.txt"%(outpath)

    query_para = {}
    content = myfunc.ReadFile(query_parafile)
    para_str = content
    if content != "":
        query_para = json.loads(content)

    try:
        name_software = query_para['name_software']
    except KeyError:
        name_software = ""


    if numseq == -1:
        numseq = myfunc.CountFastaSeq(fafile)
    if numseq_this_user == -1:
        numseq_this_user = numseq

    name_software = "topcons2"

    runjob = "%s %s/run_job.py"%(python_exec, rundir)
    scriptfile = "%s/runjob,%s,%s,%s,%s,%d.sh"%(outpath, name_software, jobid, host_ip, email, numseq)
    code_str_list = []
    code_str_list.append("#!/bin/bash")
    cmdline = "%s %s -outpath %s -tmpdir %s -jobid %s "%(runjob, fafile, outpath, datapath, jobid)
    if email != "":
        cmdline += "-email \"%s\" "%(email)
    if base_www_url != "":
        cmdline += "-baseurl \"%s\" "%(base_www_url)
    if g_params['isForceRun']:
        cmdline += "-force "
    if g_params['isOnlyGetCache']:
        cmdline += "-only-get-cache "
    code_str_list.append(cmdline)

    code = "\n".join(code_str_list)
    webcom.loginfo("Write scriptfile %s"%(scriptfile), g_params['debugfile'])

    myfunc.WriteFile(code, scriptfile, mode="w", isFlush=True)
    os.chmod(scriptfile, 0o755)

    webcom.loginfo("Getting priority", g_params['debugfile'])
    priority = myfunc.GetSuqPriority(numseq_this_user)

    if email in g_params['vip_user_list']:
        priority = 999999999.0

    webcom.loginfo("priority=%d"%(priority), g_params['debugfile'])

    query_para['queue_method'] = "slurm" # 2020-12-01, since suq is not working on CentOS8, change to slurm

    if 'queue_method' in query_para and query_para['queue_method'] == 'slurm':
        st1 = SubmitSlurmJob(datapath, outpath, priority, scriptfile)
    else:
        st1 = SubmitSuqJob(suq_basedir, datapath, outpath, priority, scriptfile)

    return st1
#}}}
def SubmitSuqJob(suq_basedir, datapath, outpath, priority, scriptfile):#{{{
    webcom.loginfo("Entering SubmitSuqJob()", g_params['debugfile'])
    rmsg = ""
    cmd = [suq_exec,"-b", suq_basedir, "run", "-d", outpath, "-p", "%d"%(priority), scriptfile]
    cmdline = " ".join(cmd)
    webcom.loginfo("cmdline: %s\n\n"%(cmdline), g_params['debugfile'])
    MAX_TRY = 5
    cnttry = 0
    isSubmitSuccess = False
    while cnttry < MAX_TRY:
        webcom.loginfo("run cmd: cnttry = %d, MAX_TRY=%d\n"%(cnttry,
            MAX_TRY), g_params['debugfile'])
        (isSubmitSuccess, t_runtime) = webcom.RunCmd(cmd, g_params['debugfile'], g_params['debugfile'])
        if isSubmitSuccess:
            break
        cnttry += 1
        time.sleep(0.05+cnttry*0.03)
    if isSubmitSuccess:
        webcom.loginfo("Leaving SubmitSuqJob() with success\n", g_params['debugfile'])
        return 0
    else:
        webcom.loginfo("Leaving SubmitSuqJob() with error\n\n", g_params['debugfile'])
        return 1
#}}}
def SubmitSlurmJob(datapath, outpath, priority, scriptfile):#{{{
    webcom.loginfo("Entering SubmitSlurmJob()", g_params['debugfile'])
    rmsg = ""
    os.chdir(outpath)
    cmd = ['sbatch', scriptfile]
    cmdline = " ".join(cmd)
    webcom.loginfo("cmdline: %s\n\n"%(cmdline), g_params['debugfile'])
    MAX_TRY = 2
    cnttry = 0
    isSubmitSuccess = False
    while cnttry < MAX_TRY:
        webcom.loginfo("run cmd: cnttry = %d, MAX_TRY=%d\n"%(cnttry,
            MAX_TRY), g_params['debugfile'])
        (isSubmitSuccess, t_runtime) = webcom.RunCmd(cmd, g_params['debugfile'], g_params['debugfile'])
        if isSubmitSuccess:
            break
        cnttry += 1
        time.sleep(0.05+cnttry*0.03)
    if isSubmitSuccess:
        webcom.loginfo("Leaving SubmitSlurmJob() with success\n", g_params['debugfile'])
        return 0
    else:
        webcom.loginfo("Leaving SubmitSlurmJob() with error\n\n", g_params['debugfile'])
        return 1
#}}}
def main(g_params):#{{{
    argv = sys.argv
    numArgv = len(argv)
    if numArgv < 2:
        PrintHelp()
        return 1

    rmsg = ""
    outpath = ""
    jobid = ""
    datapath = ""
    numseq = -1
    numseq_this_user = -1
    email = ""
    host_ip = ""
    base_www_url = ""
    i = 1
    isNonOptionArg=False
    while i < numArgv:
        if isNonOptionArg == True:
            webcom.loginfo("Error! Wrong argument: %s"(argv[i]), gen_errfile)
            return 1
            isNonOptionArg = False
            i += 1
        elif argv[i] == "--":
            isNonOptionArg = True
            i += 1
        elif argv[i][0] == "-":
            if argv[i] in ["-h", "--help"]:
                PrintHelp()
                return 1
            elif argv[i] in ["-outpath", "--outpath"]:
                (outpath, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-email", "--email"]:
                (email, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-host", "--host"]:
                (host_ip, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-nseq", "--nseq"]:
                (numseq, i) = myfunc.my_getopt_int(argv, i)
            elif argv[i] in ["-nseq-this-user", "--nseq-this-user"]:
                (numseq_this_user, i) = myfunc.my_getopt_int(argv, i)
            elif argv[i] in ["-baseurl", "--baseurl"]:
                (base_www_url, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-jobid", "--jobid"] :
                (jobid, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-datapath", "--datapath"] :
                (datapath, i) = myfunc.my_getopt_str(argv, i)
            elif argv[i] in ["-force", "--force"]:
                g_params['isForceRun'] = True
                i += 1
            elif argv[i] in ["-only-get-cache", "--only-get-cache"]:
                g_params['isOnlyGetCache'] = True
                i += 1
            elif argv[i] in ["-q", "--q"]:
                g_params['isQuiet'] = True
                i += 1
            else:
                webcom.loginfo("Error! Wrong argument: %s"(argv[i]), gen_errfile)
                return 1
        else:
            webcom.loginfo("Error! Wrong argument: %s"(argv[i]), gen_errfile)
            return 1

    if outpath == "":
        webcom.loginfo("outpath not set. exit", gen_errfile)
        return 1
    elif not os.path.exists(outpath):
        try:
            os.makedirs(outpath)
        except:
            webcom.loginfo("Failed to createt outpath=%s. exit"%(outpath), gen_errfile)
            return 1

    if jobid == "":
        webcom.loginfo("%s: jobid not set. exit"%(sys.argv[0]), gen_errfile)
        return 1

    if datapath == "":
        webcom.loginfo("%s: datapath not set. exit"%(sys.argv[0]), gen_errfile)
        return 1
    elif not os.path.exists(datapath):
        webcom.loginfo("%s: datapath does not exist. exit"%(sys.argv[0]), gen_errfile)
        return 1
    elif not os.path.exists("%s/query.fa"%(datapath)):
        webcom.loginfo("%s: file %s/query.fa does not exist. exit"%(sys.argv[0], datapath), gen_errfile)
        return 1


    if os.path.exists(vip_email_file):
        g_params['vip_user_list'] = myfunc.ReadIDList(vip_email_file)
    g_params['debugfile'] = "%s/debug.log"%(outpath)

    webcom.loginfo("Go to SubmitJobToQueue()", g_params['debugfile'])
    return SubmitJobToQueue(jobid, datapath, outpath, numseq, numseq_this_user,
            email, host_ip, base_www_url)

#}}}

def InitGlobalParameter():#{{{
    g_params = {}
    g_params['isQuiet'] = True
    g_params['isForceRun'] = False
    g_params['isOnlyGetCache'] = False
    g_params['vip_user_list'] = []
    return g_params
#}}}
if __name__ == '__main__' :
    g_params = InitGlobalParameter()
    sys.exit(main(g_params))

