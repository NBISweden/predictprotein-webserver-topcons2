#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" daemon to submit jobs and retrieve results to/from remote servers """
import os
import sys
import time
import json
import shutil
import hashlib
import random
import fcntl

rundir = os.path.dirname(os.path.realpath(__file__))
webserver_root = os.path.realpath("%s/../../../" % (rundir))
activate_env = f"{webserver_root}/env/bin/activate_this.py"
exec(compile(open(activate_env, "r").read(), activate_env, 'exec'), dict(__file__=activate_env))
from libpredweb import myfunc
from libpredweb import webserver_common as webcom
from libpredweb import qd_fe_common as qdcom
from suds.client import Client

TZ = webcom.TZ
os.environ['TZ'] = TZ
time.tzset()

# make sure that only one instance of the script is running
# this code is working
progname = os.path.basename(__file__)
rootname_progname = os.path.splitext(progname)[0]
lockname = os.path.realpath(__file__).replace(" ", "").replace("/", "-")
lock_file = f"/tmp/{lockname}.lock"
fp = open(lock_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print(f"Another instance of {progname} is running", file=sys.stderr)
    sys.exit(1)

contact_email = "nanjiang.shu@scilifelab.se"

usage_short = """
Usage: %s
""" % (sys.argv[0])

usage_ext = """
Description:
    Daemon to submit jobs and retrieve results to/from remote servers
    run periodically
    At the end of each run generate a runlog file with the status of all jobs

OPTIONS:
  -h, --help    Print this help message and exit

Created 2015-03-25, updated 2017-03-01, Nanjiang Shu
"""
usage_exp = """
"""

basedir = os.path.realpath("%s/.."%(rundir)) # path of the application, i.e. pred/
path_static = "%s/static"%(basedir)
path_log = "%s/static/log"%(basedir)
path_stat = "%s/stat"%(path_log)
path_result = "%s/static/result"%(basedir)
path_cache = "%s/static/result/cache"%(basedir)
name_cachedir = 'cache'
computenodefile = "%s/config/computenode.txt"%(basedir)
vip_email_file = "%s/config/vip_email.txt"%(basedir) 
blastdir = "%s/%s"%(rundir, "soft/topcons2_webserver/tools/blast-2.2.26")
os.environ['SCAMPI_DIR'] = "/server/scampi"
os.environ['MODHMM_BIN'] = "/server/modhmm/bin"
os.environ['BLASTMAT'] = "%s/data"%(blastdir)
os.environ['BLASTBIN'] = "%s/bin"%(blastdir)
os.environ['BLASTDB'] = "%s/%s"%(rundir, "soft/topcons2_webserver/database/blast/")
gen_errfile = "%s/static/log/%s.err"%(basedir, progname)
gen_logfile = "%s/static/log/%s.log"%(basedir, progname)
black_iplist_file = "%s/config/black_iplist.txt"%(basedir)
finished_date_db = "%s/cached_job_finished_date.sqlite3"%(path_log)


def PrintHelp(fpout=sys.stdout):#{{{
    print(usage_short, file=fpout)
    print(usage_ext, file=fpout)
    print(usage_exp, file=fpout)#}}}


def main(g_params):  # {{{
    runjoblogfile = f"{path_log}/runjob_log.log"
    if os.path.exists(black_iplist_file):
        g_params['blackiplist'] = myfunc.ReadIDList(black_iplist_file)

    if not os.path.exists(path_cache):
        os.mkdir(path_cache)

    loop = 0
    while 1:
        # pause when cache cleaning is in progress
        if os.path.exists(f"{path_result}/CACHE_CLEANING_IN_PROGRESS"):
            continue

        # load the config file if exists
        configfile = f"{basedir}/config/config.json"
        config = {}
        if os.path.exists(configfile):
            text = myfunc.ReadFile(configfile)
            config = json.loads(text)

        if rootname_progname in config:
            g_params.update(config[rootname_progname])

        if os.path.exists(black_iplist_file):
            g_params['blackiplist'] = myfunc.ReadIDList(black_iplist_file)

        # avail_computenode is a dictionary
        avail_computenode = webcom.ReadComputeNode(computenodefile)
        g_params['vip_user_list'] = myfunc.ReadIDList2(vip_email_file, col=0)

        webcom.loginfo(f"loop {loop}", gen_logfile)

        isOldRstdirDeleted = False
        if loop % g_params['STATUS_UPDATE_FREQUENCY'][0] == g_params['STATUS_UPDATE_FREQUENCY'][1]:
            qdcom.RunStatistics(g_params)
            isOldRstdirDeleted = webcom.DeleteOldResult(
                    path_result, path_log,
                    gen_logfile, MAX_KEEP_DAYS=g_params['MAX_KEEP_DAYS'])
            webcom.CleanCachedResult(path_static, name_cachedir, gen_logfile, gen_errfile)
        if loop % g_params['CLEAN_SERVER_FREQUENCY'][0] == g_params['CLEAN_SERVER_FREQUENCY'][1]:
            webcom.CleanServerFile(path_static, gen_logfile, gen_errfile)

        if 'DEBUG_ARCHIVE' in g_params and g_params['DEBUG_ARCHIVE']:
            webcom.loginfo("Run ArchiveLogFile, path_log=%s, threshold_logfilesize=%d"%(
                path_log, g_params['threshold_logfilesize']), gen_logfile)
        webcom.ArchiveLogFile(path_log, g_params['threshold_logfilesize'], g_params)

        qdcom.CreateRunJoblog(loop, isOldRstdirDeleted, g_params)

        # Get number of jobs submitted to the remote server based on the
        # runjoblogfile
        runjobidlist = myfunc.ReadIDList2(runjoblogfile, 0)
        remotequeueDict = {}
        for node in avail_computenode:
            remotequeueDict[node] = []
        for jobid in runjobidlist:
            rstdir = os.path.join(path_result, jobid)
            remotequeue_idx_file = f"{rstdir}/remotequeue_seqindex.txt"
            if os.path.exists(remotequeue_idx_file):
                content = myfunc.ReadFile(remotequeue_idx_file)
                lines = content.split('\n')
                for line in lines:
                    strs = line.split('\t')
                    if len(strs) >= 5:
                        node = strs[1]
                        remotejobid = strs[2]
                        if node in remotequeueDict:
                            remotequeueDict[node].append(remotejobid)

        cntSubmitJobDict = {}  # format of cntSubmitJobDict {'node_ip': INT, 'node_ip': INT}
        for node in avail_computenode:
            queue_method = avail_computenode[node]['queue_method']
            num_queue_job = len(remotequeueDict[node])
            if num_queue_job >= 0:
                cntSubmitJobDict[node] = [num_queue_job,
                        g_params['MAX_SUBMIT_JOB_PER_NODE'], queue_method] #[num_queue_job, max_allowed_job]
            else:
                cntSubmitJobDict[node] = [0,
                        g_params['MAX_SUBMIT_JOB_PER_NODE'], queue_method] #[num_queue_job, max_allowed_job]

# entries in runjoblogfile includes jobs in queue or running
        dt_runjoblog = myfunc.ReadRunJobLog(runjoblogfile)
        reordered_runjobidlist = runjobidlist
        # randomize the order of runjob some time, give some big jobs also a
        # chance to run
        if (loop % g_params['RAND_RUNJOB_ORDER_FREQ'][0] == g_params['RAND_RUNJOB_ORDER_FREQ'][1]):
            random.shuffle(reordered_runjobidlist)

        for jobid in reordered_runjobidlist:
            [status_this_job, jobname, ip, email, numseq, method_submission,
                    submit_date_str, start_date_str, finish_date_str,
                    total_numseq_of_user, priority] = dt_runjoblog[jobid]
            numseq_this_user = total_numseq_of_user
            rstdir = os.path.join(path_result, jobid)
            webcom.loginfo(f"CompNodeStatus: {cntSubmitJobDict}\n", gen_logfile)
            runjob_lockfile = "%s/%s/%s.lock"%(path_result, jobid, "runjob.lock")
            if os.path.exists(runjob_lockfile):
                msg = "runjob_lockfile %s exists, ignore the job %s" %(runjob_lockfile, jobid)
                webcom.loginfo(msg, gen_logfile)
                continue
            if (webcom.IsHaveAvailNode(cntSubmitJobDict)
                    or (numseq <= g_params['THRESHOLD_SMALL_JOB']
                        and method_submission == "web")
                    or not webcom.IsCacheProcessingFinished(rstdir)
                    ):
                if not g_params['DEBUG_NO_SUBMIT']:
                    qdcom.SubmitJob(jobid, cntSubmitJobDict, numseq_this_user, g_params)
            qdcom.GetResult(jobid, g_params)  # the start tagfile is written when got the first result
            qdcom.CheckIfJobFinished(jobid, numseq, email, g_params)


        webcom.loginfo("sleep for %d seconds\n"%(g_params['SLEEP_INTERVAL']), gen_logfile)
        time.sleep(g_params['SLEEP_INTERVAL'])
        loop += 1

    return 0
# }}}


def InitGlobalParameter():  # {{{
    g_params = {}
    g_params['isQuiet'] = True
    g_params['blackiplist'] = []
    g_params['vip_user_list'] = []
    g_params['DEBUG'] = False
    g_params['DEBUG_NO_SUBMIT'] = False
    g_params['DEBUG_CACHE'] = False
    g_params['SLEEP_INTERVAL'] = 5    # sleep interval in seconds
    g_params['MAX_SUBMIT_JOB_PER_NODE'] = 400
    g_params['MAX_KEEP_DAYS'] = 30
    g_params['THRESHOLD_SMALL_JOB'] = 10  # max number of sequences to be considered as small job
    g_params['MAX_RESUBMIT'] = 2
    g_params['MAX_SUBMIT_TRY'] = 3
    g_params['MAX_TIME_IN_REMOTE_QUEUE'] = 3600*24  # one day in seconds
    g_params['MAX_CACHE_PROCESS'] = 200 # process at the maximum this cached sequences in one loop
    g_params['STATUS_UPDATE_FREQUENCY'] = [800, 50]  # updated by if loop%$1 == $2
    g_params['RAND_RUNJOB_ORDER_FREQ'] = [100, 50]  # updated by if loop%$1 == $2
    g_params['CLEAN_SERVER_FREQUENCY'] = [50, 0]  # updated by if loop%$1 == $2
    g_params['FORMAT_DATETIME'] = webcom.FORMAT_DATETIME
    g_params['threshold_logfilesize'] = 20*1024*1024
    g_params['script_scampi'] = "%s/%s/%s" % (rundir, "other", "mySCAMPI_run.pl")
    g_params['name_server'] = "TOPCONS2"
    g_params['path_static'] = path_static
    g_params['path_result'] = path_result
    g_params['path_log'] = path_log
    g_params['path_cache'] = path_cache
    g_params['gen_logfile'] = gen_logfile
    g_params['gen_errfile'] = gen_errfile
    g_params['contact_email'] = contact_email
    g_params['vip_email_file'] = vip_email_file
    g_params['UPPER_WAIT_TIME_IN_SEC'] = 0  # wait time before it will be handled by qd_fe
    g_params['webserver_root'] = webserver_root
    g_params['THRESHOLD_NUMSEQ_CHECK_IF_JOB_FINISH'] = 100 # threshold of numseq for the job to run CheckIfJobFinished in a separate process
    g_params['finished_date_db'] = finished_date_db
    return g_params
# }}}


if __name__ == '__main__':
    g_params = InitGlobalParameter()
    date_str = time.strftime(g_params['FORMAT_DATETIME'])
    print("\n#%s#\n[Date: %s] qd_fe.py restarted" % ('='*80, date_str))
    sys.stdout.flush()
    sys.exit(main(g_params))
