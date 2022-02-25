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

def GetResult(jobid):#{{{
    # retrieving result from the remote server for this job
    webcom.loginfo("GetResult for %s.\n" %(jobid), gen_logfile)
    rstdir = "%s/%s"%(path_result, jobid)
    outpath_result = "%s/%s"%(rstdir, jobid)
    if not os.path.exists(outpath_result):
        os.mkdir(outpath_result)

    remotequeue_idx_file = "%s/remotequeue_seqindex.txt"%(rstdir)

    torun_idx_file = "%s/torun_seqindex.txt"%(rstdir) # ordered seq index to run
    finished_idx_file = "%s/finished_seqindex.txt"%(rstdir)
    failed_idx_file = "%s/failed_seqindex.txt"%(rstdir)

    starttagfile = "%s/%s"%(rstdir, "runjob.start")
    cnttry_idx_file = "%s/cntsubmittry_seqindex.txt"%(rstdir)#index file to keep log of tries
    tmpdir = "%s/tmpdir"%(rstdir)
    finished_seq_file = "%s/finished_seqs.txt"%(outpath_result)

    finished_info_list = [] #[info for finished record]
    finished_idx_list = [] # [origIndex]
    failed_idx_list = []    # [origIndex]
    resubmit_idx_list = []  # [origIndex]
    keep_queueline_list = [] # [line] still in queue
    runjob_errfile = "%s/%s"%(rstdir, "runjob.err")
    runjob_logfile = "%s/%s"%(rstdir, "runjob.log")

    cntTryDict = {}
    if os.path.exists(cnttry_idx_file):
        try:
            with open(cnttry_idx_file, 'r') as fpin:
                cntTryDict = json.load(fpin)
        except ValueError: #rewrite the cnttry_idx_file if it is corrupted
            myfunc.WriteFile("",cnttry_idx_file, "w", isFlush=True)

    # in case of missing queries, if remotequeue_idx_file is empty  but the job
    # is still not finished, force re-creating torun_idx_file
    if g_params['DEBUG']:
        try:
            webcom.loginfo("DEBUG: %s: remotequeue_idx_file=%s, size(remotequeue_idx_file)=%d, content=\"%s\"\n" %(jobid, remotequeue_idx_file, os.path.getsize(remotequeue_idx_file), myfunc.ReadFile(remotequeue_idx_file)), gen_logfile)
        except:
            pass
    if ((not os.path.exists(remotequeue_idx_file) or#{{{
        os.path.getsize(remotequeue_idx_file)<1)):
        idlist1 = []
        idlist2 = []
        if os.path.exists(finished_idx_file):
           idlist1 =  myfunc.ReadIDList(finished_idx_file)
        if os.path.exists(failed_idx_file):
           idlist2 =  myfunc.ReadIDList(failed_idx_file)

        completed_idx_set = set(idlist1 + idlist2)

        jobinfofile = "%s/jobinfo"%(rstdir)
        jobinfo = myfunc.ReadFile(jobinfofile).strip()
        jobinfolist = jobinfo.split("\t")
        if len(jobinfolist) >= 8:
            numseq = int(jobinfolist[3])



        if g_params['DEBUG']:
            webcom.loginfo("DEBUG: len(completed_idx_set)=%d+%d=%d, numseq=%d\n"%(len(idlist1), len(idlist2), len(completed_idx_set), numseq), gen_logfile)


        if len(completed_idx_set) < numseq:
            all_idx_list = [str(x) for x in range(numseq)]
            torun_idx_str_list = list(set(all_idx_list)-completed_idx_set)
            for idx in torun_idx_str_list:
                try:
                    cntTryDict[int(idx)] += 1
                except:
                    cntTryDict[int(idx)] = 1
                    pass
            myfunc.WriteFile("\n".join(torun_idx_str_list)+"\n", torun_idx_file, "w", True)

            if g_params['DEBUG']:
                webcom.loginfo("DEBUG: recreate torun_idx_file: jobid = %s, numseq=%d, len(completed_idx_set)=%d, len(torun_idx_str_list)=%d\n"%(jobid, numseq, len(completed_idx_set), len(torun_idx_str_list)), gen_logfile)
        else:
            myfunc.WriteFile("", torun_idx_file, "w", True)
    else:
        if g_params['DEBUG']:
            webcom.loginfo("DEBUG: %s: remotequeue_idx_file %s is not empty\n" %(jobid, remotequeue_idx_file), gen_logfile)
#}}}

    text = ""
    if os.path.exists(remotequeue_idx_file):
        text = myfunc.ReadFile(remotequeue_idx_file)
    if text == "":
        return 1
    lines = text.split("\n")

    nodeSet = set([])
    for i in range(len(lines)):
        line = lines[i]
        if not line or line[0] == "#":
            continue
        strs = line.split("\t")
        if len(strs) != 6:
            continue
        node = strs[1]
        nodeSet.add(node)

    myclientDict = {}
    for node in nodeSet:
        wsdl_url = "http://%s/pred/api_submitseq/?wsdl"%(node)
        try:
            myclient = Client(wsdl_url, cache=None, timeout=30)
            myclientDict[node] = myclient
        except:
            webcom.loginfo("Failed to access %s"%(wsdl_url), gen_errfile)
            pass


    for i in range(len(lines)):#{{{
        line = lines[i]

        if g_params['DEBUG']:
            webcom.loginfo("DEBUG: Process %s"%(line), gen_logfile)
        if not line or line[0] == "#":
            if g_params['DEBUG']:
                webcom.loginfo("DEBUG: line empty or line[0] = '#', ignore", gen_logfile)
            continue
        strs = line.split("\t")
        if len(strs) != 6:
            if g_params['DEBUG']:
                webcom.loginfo("DEBUG: len(strs)=%d (!=6), ignore\n"%(len(strs)), gen_logfile)
            continue
        origIndex = int(strs[0])
        node = strs[1]
        remote_jobid = strs[2]
        description = strs[3]
        seq = strs[4]
        submit_time_epoch = float(strs[5])
        subfoldername_this_seq = "seq_%d"%(origIndex)
        outpath_this_seq = "%s/%s"%(outpath_result, "seq_%d"%origIndex)

        try:
            myclient = myclientDict[node]
        except KeyError:
            if g_params['DEBUG']:
                webcom.loginfo("DEBUG: node (%s) not found in myclientDict, ignore"%(node), gen_logfile)
            keep_queueline_list.append(line)
            continue
        try:
            rtValue = myclient.service.checkjob(remote_jobid)
        except Exception as e:
            msg = "checkjob(%s) at node %s failed with errmsg %s"%(remote_jobid, node, str(e))
            webcom.loginfo(msg, gen_logfile)
            rtValue = []
            pass
        isSuccess = False
        isFinish_remote = False
        status = ""
        if len(rtValue) >= 1:
            ss2 = rtValue[0]
            if len(ss2)>=3:
                status = ss2[0]
                result_url = ss2[1]
                errinfo = ss2[2]

                if errinfo and errinfo.find("does not exist")!=-1:
                    if g_params['DEBUG']:
                        msg = "Failed for remote_jobid %s with errmsg %s"%(remote_jobid, str(errinfo))
                        webcom.loginfo(msg, gen_logfile)

                    isFinish_remote = True

                if status == "Finished":#{{{
                    isFinish_remote = True
                    outfile_zip = "%s/%s.zip"%(tmpdir, remote_jobid)
                    isRetrieveSuccess = False
                    myfunc.WriteFile("\tFetching result for %s/seq_%d from %s "%(
                        jobid, origIndex,result_url), gen_logfile, "a", True)
                    if myfunc.IsURLExist(result_url,timeout=5):
                        try:
                            myfunc.urlretrieve (result_url, outfile_zip, timeout=10)
                            isRetrieveSuccess = True
                            myfunc.WriteFile(" succeeded on node %s\n"%(node), gen_logfile, "a", True)
                        except:
                            myfunc.WriteFile(" failed on node %s\n"%(node), gen_logfile, "a", True)
                            pass
                    if os.path.exists(outfile_zip) and isRetrieveSuccess:
                        cmd = ["unzip", outfile_zip, "-d", tmpdir]
                        webcom.RunCmd(cmd, gen_logfile, gen_errfile)
                        rst_this_seq = "%s/%s/seq_0"%(tmpdir, remote_jobid)

                        if os.path.islink(outpath_this_seq):
                            os.unlink(outpath_this_seq)
                        elif os.path.exists(outpath_this_seq):
                            shutil.rmtree(outpath_this_seq)

                        if os.path.exists(rst_this_seq) and not os.path.exists(outpath_this_seq):
                            cmd = ["mv","-f", rst_this_seq, outpath_this_seq]
                            webcom.RunCmd(cmd, gen_logfile, gen_errfile)

                            checkfile = "%s/Topcons/topcons.png"%(outpath_this_seq)
                            fafile_this_seq =  '%s/seq.fa'%(outpath_this_seq)
                            if os.path.exists(outpath_this_seq) and os.path.exists(checkfile):
                                # relpace the seq.fa with original description
                                myfunc.WriteFile('>%s\n%s\n'%(description, seq), fafile_this_seq, 'w', True)
                                isSuccess = True

                            if isSuccess:
                                # delete the data on the remote server
                                try:
                                    rtValue2 = myclient.service.deletejob(remote_jobid)
                                except Exception as e:
                                    msg = "Failed to deletejob(%s) on node %s with errmsg %s"%(remote_jobid, node, str(e))
                                    webcom.loginfo(msg, gen_logfile)
                                    rtValue2 = []
                                    pass

                                logmsg = ""
                                if len(rtValue2) >= 1:
                                    ss2 = rtValue2[0]
                                    if len(ss2) >= 2:
                                        status = ss2[0]
                                        errmsg = ss2[1]
                                        if status == "Succeeded":
                                            logmsg = "Successfully deleted data on %s "\
                                                    "for %s"%(node, remote_jobid)
                                        else:
                                            logmsg = "Failed to delete data on %s for "\
                                                    "%s\nError message:\n%s\n"%(node, remote_jobid, errmsg)
                                else:
                                    logmsg = "Failed to call deletejob %s via WSDL on %s\n"%(remote_jobid, node)

                                # delete the zip file
                                os.remove(outfile_zip)
                                shutil.rmtree("%s/%s"%(tmpdir, remote_jobid))

                                # create or update the md5 cache
                                md5_key = hashlib.md5(seq.encode('utf-8')).hexdigest()
                                subfoldername = md5_key[:2]
                                md5_subfolder = "%s/%s"%(path_cache, subfoldername)
                                cachedir = "%s/%s/%s"%(path_cache, subfoldername, md5_key)

                                # copy the zipped folder to the cache path
                                origpath = os.getcwd()
                                os.chdir(outpath_result)
                                shutil.copytree("seq_%d"%(origIndex), md5_key)
                                cmd = ["zip", "-rq", "%s.zip"%(md5_key), md5_key]
                                webcom.RunCmd(cmd, runjob_logfile, runjob_errfile)
                                if not os.path.exists(md5_subfolder):
                                    os.makedirs(md5_subfolder)
                                shutil.move("%s.zip"%(md5_key), "%s.zip"%(cachedir))
                                shutil.rmtree(md5_key) # delete the temp folder named as md5 hash
                                os.chdir(origpath)

                                # Add the finished date to the database
                                date_str = time.strftime(g_params['FORMAT_DATETIME'])
                                MAX_TRY_INSERT_DB = 3
                                cnttry = 0
                                while cnttry < MAX_TRY_INSERT_DB:
                                    t_rv = webcom.InsertFinishDateToDB(date_str, md5_key, seq, finished_date_db)
                                    if t_rv == 0:
                                        break
                                    cnttry += 1
                                    time.sleep(random.random()/1.0)

#}}}
                elif status in ["Failed", "None"]:
                    # the job is failed for this sequence, try to re-submit
                    isFinish_remote = True
                    if g_params['DEBUG']:
                        webcom.loginfo("DEBUG: %s, status = %s\n"%(remote_jobid, status), gen_logfile)

                    cnttry = 1
                    try:
                        cnttry = cntTryDict[int(origIndex)]
                    except KeyError:
                        cnttry = 1
                        pass
                    if cnttry < g_params['MAX_RESUBMIT']:
                        myfunc.WriteFile("%d\n"%(origIndex), torun_idx_file, "a", True)
                        cntTryDict[int(origIndex)] = cnttry+1
                    else:
                        myfunc.WriteFile("%d\n"%(origIndex), failed_idx_file, "a", True)
                if status != "Wait" and not os.path.exists(starttagfile):
                    webcom.WriteDateTimeTagFile(starttagfile, runjob_logfile, runjob_errfile)

        if isSuccess:#{{{
            time_now = time.time()
            timefile = "%s/time.txt"%(outpath_this_seq)
            runtime1 = time_now - submit_time_epoch #in seconds
            runtime = webcom.ReadRuntimeFromFile(timefile, default_runtime=runtime1)
            info_finish = webcom.GetInfoFinish_TOPCONS2(outpath_this_seq,
                    origIndex, len(seq), description, source_result="newrun",
                    runtime=runtime)
            myfunc.WriteFile("\t".join(info_finish)+"\n", finished_seq_file, "a", True)
            myfunc.WriteFile("%d\n"%(origIndex), finished_idx_file, "a", True)

            #}}}

        if not isFinish_remote:
            time_in_remote_queue = time.time() - submit_time_epoch
            # for jobs queued in the remote queue more than one day (but not
            # running) delete it and try to resubmit it. This solved the
            # problem of dead jobs in the remote server due to server
            # rebooting)
            if status != "Running" and time_in_remote_queue > g_params['MAX_TIME_IN_REMOTE_QUEUE']:
                msg = "Trying to delete the job in the remote queue since time_in_remote_queue = %d and status = '%s'"%(time_in_remote_queue, status)
                webcom.loginfo(msg, gen_logfile)
                # delete the remote job on the remote server
                try:
                    rtValue2 = myclient.service.deletejob(remote_jobid)
                except Exception as e:
                    msg = "Failed to run myclient.service.deletejob(%s) on node %s with msg %s\n"%(remote_jobid, node, str(e))
                    webcom.loginfo(msg, gen_logfile)
                    rtValue2 = []
                    pass
            else:
                keep_queueline_list.append(line)
#}}}
    #Finally, write log files

    if g_params['DEBUG']:
        webcom.loginfo("DEBUG: len(keep_queueline_list)=%d\n"%(len(keep_queueline_list)), gen_logfile)

    if len(keep_queueline_list)>0:
        keep_queueline_list = list(set(keep_queueline_list))
        myfunc.WriteFile("\n".join(keep_queueline_list)+"\n", remotequeue_idx_file, "w", True);
    else:
        myfunc.WriteFile("", remotequeue_idx_file, "w", True);

    with open(cnttry_idx_file, 'w') as fpout:
        json.dump(cntTryDict, fpout)

    return 0
#}}}


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
            GetResult(jobid) # the start tagfile is written when got the first result
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
    return g_params
# }}}


if __name__ == '__main__':
    g_params = InitGlobalParameter()
    date_str = time.strftime(g_params['FORMAT_DATETIME'])
    print("\n#%s#\n[Date: %s] qd_fe.py restarted" % ('='*80, date_str))
    sys.stdout.flush()
    sys.exit(main(g_params))
