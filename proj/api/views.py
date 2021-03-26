from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.views.static import serve
from django.http import JsonResponse

from libpredweb import myfunc
from libpredweb import webserver_common as webcom
import os
import time
import json


# Create your views here.
def index(request):#{{{
    return HttpResponse("Thanks")
#}}}

def GetData():# {{{
    """
    Return a dictionary containing submitted entries
    """
    job_dict = {}
    methodList = ["topcons2","proq3", "pconsc3", "subcons", "scampi2", "boctopus2"]
    for method in methodList:
        path_log = "/var/www/html/%s/proj/pred/static/log"%(method)
        file1 = os.path.join(path_log, "all_submitted_seq.log")
        file2 = os.path.join(path_log, "submitted_seq.log")
        if os.path.exists(file1):
            submitjoblogfile = file1
        else:
            submitjoblogfile = file2

        dt = myfunc.ReadSubmittedLogFile(submitjoblogfile)
        newdt = {}
        for jobid in dt.keys():
            submit_date_str = dt[jobid][0]
            client_ip = dt[jobid][2]
            submit_date = webcom.datetime_str_to_time(submit_date_str)
#             li = submit_date_str.split()[:2]
#             submit_date = "".join(li).replace('-','').replace(':','')
            newdt[jobid] = [client_ip, submit_date, submit_date_str]
        job_dict[method] = newdt

    return job_dict
# }}}


def check_job_dict():# {{{
    """debugging function, check the content of the job_dict
    """
    job_dict = GetData()
    usercount_dict = {}
    for method in job_dict.keys():
        usercount_dict[method] = {}
        ipList = []
        submitdateList = []
        for jobid in job_dict[method].keys():
            ip =  job_dict[method][jobid][0]
            submit_date =  job_dict[method][jobid][1]
            if submit_date is None:
                print(job_dict[method][jobid])
            ipList.append(job_dict[method][jobid][0])
            submitdateList.append(job_dict[method][jobid][1])
        submitdateList.sort()
        usercount_dict[method]['total'] = len(set(ipList))
        usercount_dict[method]['start'] = sortedSubmitDateList[0].strftime(webcom.FORMAT_DATETIME)
        usercount_dict[method]['end'] = sortedSubmitDateList[-1].strftime(webcom.FORMAT_DATETIME)
# }}}

def count_users(request):# {{{
    job_dict = GetData()
    usercount_dict = {}
    for method in job_dict.keys():
        usercount_dict[method] = {}
        ipList = []
        submitdateList = []
        for jobid in job_dict[method].keys():
            ipList.append(job_dict[method][jobid][0])
            submitdateList.append(job_dict[method][jobid][1])
        submitdateList.sort()
        usercount_dict[method]['total'] = len(set(ipList))
        usercount_dict[method]['start'] = submitdateList[0].strftime(webcom.FORMAT_DATETIME)
        usercount_dict[method]['end'] = submitdateList[-1].strftime(webcom.FORMAT_DATETIME)

    return JsonResponse(usercount_dict)# }}}

def count_users_with_start_date(request, startdate_str=""):
    job_dict = GetData()
    usercount_dict = {}
    start_date = webcom.datetime_str_to_time(startdate_str, isSetDefault=False)
    if start_date is None:
        usercount_dict = {"Wrong startdate"}
    else:
        for method in job_dict.keys():
            usercount_dict[method] = {}
            ipList = []
            submitdateList = []
            for jobid in job_dict[method].keys():
                submit_date = job_dict[method][jobid][1]
                if submit_date >= startdate:
                    ipList.append(job_dict[method][jobid][0])
                    submitdateList.append(submit_date)
            submitdateList.sort()
            usercount_dict[method]['total'] = len(set(ipList))
            usercount_dict[method]['start'] = submitdateList[0].strftime(webcom.FORMAT_DATETIME)
            usercount_dict[method]['end'] = submitdateList[-1].strftime(webcom.FORMAT_DATETIME)
    return JsonResponse(usercount_dict)

def count_users_with_start_end_date(request, startdate="", enddate=""):
    dt = {}
    dt['total'] = 1000
    dt['start'] = startdate
    dt['end'] = enddate
    return JsonResponse(dt)

