#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description: show job queue status for all webservers

import os
import sys
import shutil
import subprocess
import pwd
from libpredweb import myfunc
from libpredweb import webserver_common
from datetime import datetime
from pytz import timezone

import tabulate
TZ = "Europe/Stockholm"

progname = os.path.basename(__file__)
rootname_progname = os.path.splitext(progname)[0]
lockname = os.path.realpath(__file__).replace(" ", "").replace("/", "-")
import fcntl
lock_file = "/tmp/%s.lock"%(lockname)
fp = open(lock_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("Another instance of %s is running"%(progname), file=sys.stderr)
    sys.exit(1)

usage="""
usage: %s server_name [server_name ...]

"""%(sys.argv[0])

default_server_list = [
        "scampi2",
        "topcons2",
        "subcons",
        "proq3",
        "prodres",
        "pconsc3",
        "boctopus2",
        "tmbmodel"

        ]

server_list = default_server_list[:]
if len(sys.argv) >= 2:
    for ss in sys.argv[1:]:
        server_list.append(ss.lower())


#print "server_list = ", server_list


def GetBaseDir(server_name):# {{{
    """Get basedir of the server given server name
    """
    basedir =  "/var/www/html/%s/proj/pred"%(server_name)
    if os.path.exists(basedir):
        return basedir
    else:
        sys.stderr.write("unrecognized server name \"%s\"\n"%(server_name))
        return ""

# }}}
def GetJobCounter(logfile_query, logfile_finished_jobid, path_result):#{{{
# get job counter for all
# get the table from runlog, 
# for queued or running jobs, if source=web and numseq=1, check again the tag file in
# each individual folder, since they are queued locally
    jobcounter = {}

    jobcounter['queued'] = 0
    jobcounter['running'] = 0
    jobcounter['finished'] = 0
    jobcounter['failed'] = 0
    jobcounter['nojobfolder'] = 0 #of which the folder jobid does not exist

    jobcounter['queued_idlist'] = []
    jobcounter['running_idlist'] = []
    jobcounter['finished_idlist'] = []
    jobcounter['failed_idlist'] = []
    jobcounter['nojobfolder_idlist'] = []


    hdl = myfunc.ReadLineByBlock(logfile_query)
    if hdl.failure:
        return jobcounter
    else:
        finished_job_dict = myfunc.ReadFinishedJobLog(logfile_finished_jobid)
        finished_jobid_set = set([])
        failed_jobid_set = set([])
        for jobid in finished_job_dict:
            status = finished_job_dict[jobid][0]
            rstdir = "%s/%s"%(path_result, jobid)
            if status == "Finished":
                finished_jobid_set.add(jobid)
            elif status == "Failed":
                failed_jobid_set.add(jobid)
        lines = hdl.readlines()
        current_time = datetime.now(timezone(TZ))
        while lines != None:
            for line in lines:
                strs = line.split("\t")
                if len(strs) < 7:
                    continue
                ip = strs[2]

                submit_date_str = strs[0]
                isValidSubmitDate = True
                try:
                    submit_date = webserver_common.datetime_str_to_time(submit_date_str)
                except ValueError:
                    isValidSubmitDate = False

                if not isValidSubmitDate:
                    continue

                diff_date = current_time - submit_date
                jobid = strs[1]
                rstdir = "%s/%s"%(path_result, jobid)

                if jobid in finished_jobid_set:
                    jobcounter['finished'] += 1
                    jobcounter['finished_idlist'].append(jobid)
                elif jobid in failed_jobid_set:
                    jobcounter['failed'] += 1
                    jobcounter['failed_idlist'].append(jobid)
                else:
                    finishtagfile = "%s/%s"%(rstdir, "runjob.finish")
                    failtagfile = "%s/%s"%(rstdir, "runjob.failed")
                    starttagfile = "%s/%s"%(rstdir, "runjob.start")
                    if not os.path.exists(rstdir):
                        jobcounter['nojobfolder'] += 1
                        jobcounter['nojobfolder_idlist'].append(jobid)
                    elif os.path.exists(failtagfile):
                        jobcounter['failed'] += 1
                        jobcounter['failed_idlist'].append(jobid)
                    elif os.path.exists(finishtagfile):
                        jobcounter['finished'] += 1
                        jobcounter['finished_idlist'].append(jobid)
                    elif os.path.exists(starttagfile):
                        jobcounter['running'] += 1
                        jobcounter['running_idlist'].append(jobid)
                    else:
                        jobcounter['queued'] += 1
                        jobcounter['queued_idlist'].append(jobid)
            lines = hdl.readlines()
        hdl.close()
    return jobcounter
#}}}
def GetServerQueueStatus(server_name):# {{{
    basedir = GetBaseDir(server_name)
    if basedir != "":
        path_log = "%s/static/log"%(basedir)
        path_result = "%s/static/result"%(basedir)
        logfile_query = "%s/submitted_seq.log"%(path_log)
        logfile_finished_jobid = "%s/finished_jobid.log"%(path_log)
        jobcounter = GetJobCounter(logfile_query, logfile_finished_jobid, path_result)
        return jobcounter
# }}}

lst_status = ["queued", "running", "finished", "failed"]
header_line = ["Webserver"] + lst_status
data_line = []

for server_name in server_list:
    jobcounter = GetServerQueueStatus(server_name)
    lst = [server_name]
    for ss in lst_status:
        try:
            value = str(jobcounter[ss])
        except:
            value = "NA"
        lst.append(value)
    data_line.append(lst)

content = tabulate.tabulate(data_line, header_line, 'grid')
print(content)


