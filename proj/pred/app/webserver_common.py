#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description:
#   A collection of classes and functions used by web-servers
#
# Author: Nanjiang Shu (nanjiang.shu@scilifelab.se)
#
# Address: Science for Life Laboratory Stockholm, Box 1031, 17121 Solna, Sweden

import os
import sys
import re
rundir = os.path.dirname(os.path.realpath(__file__))
import myfunc
import time
from datetime import datetime
from dateutil import parser as dtparser
from pytz import timezone
import tabulate
import shutil
import logging
import subprocess
import sqlite3
from nanjianglib.timeit import timeit


TZ = "Europe/Stockholm"
FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S %Z"
def IsCacheProcessingFinished(rstdir):# {{{
    """Check whether the jobdir is still under cache processing"""
    forceruntagfile = "%s/forcerun"%(rstdir)
    cache_process_finish_tagfile = "%s/cache_processed.finish"%(rstdir)
    if os.path.exists(forceruntagfile):
        isForceRun = True
    else:
        isForceRun = False
    if isForceRun or os.path.exists(cache_process_finish_tagfile):
        isCacheProcessingFinished = True
    else:
        isCacheProcessingFinished = False
    return isCacheProcessingFinished
# }}}
def IsHaveAvailNode(cntSubmitJobDict):#{{{
    """
    Check if there are available slots in any of the computational node
    format of cntSubmitJobDict {'node_ip': INT, 'node_ip': INT}  
    """
    for node in cntSubmitJobDict:
        [num_queue_job, max_allowed_job] = cntSubmitJobDict[node]
        if num_queue_job < max_allowed_job:
            return True
    return False
#}}}
def get_job_status(jobid, path_result):#{{{
    status = "";
    rstdir = "%s/%s"%(path_result, jobid)
    starttagfile = "%s/%s"%(rstdir, "runjob.start")
    finishtagfile = "%s/%s"%(rstdir, "runjob.finish")
    failedtagfile = "%s/%s"%(rstdir, "runjob.failed")
    if os.path.exists(failedtagfile):
        status = "Failed"
    elif os.path.exists(finishtagfile):
        status = "Finished"
    elif os.path.exists(starttagfile):
        status = "Running"
    elif os.path.exists(rstdir):
        status = "Wait"
    return status
#}}}

@timeit
def WriteSubconsTextResultFile(outfile, outpath_result, maplist,#{{{
        runtime_in_sec, base_www_url, statfile=""):
    try:
        fpout = open(outfile, "w")
        if statfile != "":
            fpstat = open(statfile, "w")

        date_str = time.strftime(FORMAT_DATETIME)
        print("##############################################################################", file=fpout)
        print("Subcons result file", file=fpout)
        print("Generated from %s at %s"%(base_www_url, date_str), file=fpout)
        print("Total request time: %.1f seconds."%(runtime_in_sec), file=fpout)
        print("##############################################################################", file=fpout)
        cnt = 0
        for line in maplist:
            strs = line.split('\t')
            subfoldername = strs[0]
            length = int(strs[1])
            desp = strs[2]
            seq = strs[3]
            seqid = myfunc.GetSeqIDFromAnnotation(desp)
            print("Sequence number: %d"%(cnt+1), file=fpout)
            print("Sequence name: %s"%(desp), file=fpout)
            print("Sequence length: %d aa."%(length), file=fpout)
            print("Sequence:\n%s\n\n"%(seq), file=fpout)

            rstfile = "%s/%s/%s/query_0.csv"%(outpath_result, subfoldername, "plot")

            if os.path.exists(rstfile):
                content = myfunc.ReadFile(rstfile).strip()
                lines = content.split("\n")
                if len(lines) >= 6:
                    header_line = lines[0].split("\t")
                    if header_line[0].strip() == "":
                        header_line[0] = "Method"
                        header_line = [x.strip() for x in header_line]

                    data_line = []
                    for i in range(1, len(lines)):
                        strs1 = lines[i].split("\t")
                        strs1 = [x.strip() for x in strs1]
                        data_line.append(strs1)

                    content = tabulate.tabulate(data_line, header_line, 'plain')
            else:
                content = ""
            if content == "":
                content = "***No prediction could be produced with this method***"

            print("Prediction results:\n\n%s\n\n"%(content), file=fpout)

            print("##############################################################################", file=fpout)
            cnt += 1

    except IOError:
        print("Failed to write to file %s"%(outfile))
#}}}

@timeit
def WriteTOPCONSTextResultFile(outfile, outpath_result, maplist,#{{{
        runtime_in_sec, base_www_url, statfile=""):
    try:
        methodlist = ['TOPCONS', 'OCTOPUS', 'Philius', 'PolyPhobius', 'SCAMPI',
                'SPOCTOPUS', 'Homology']
        fpout = open(outfile, "w")

        fpstat = None
        num_TMPro_cons = 0
        num_TMPro_any = 0
        num_nonTMPro_cons = 0
        num_nonTMPro_any = 0
        num_SPPro_cons = 0
        num_SPPro_any = 0

        if statfile != "":
            fpstat = open(statfile, "w")

        date_str = time.strftime(FORMAT_DATETIME)
        print("##############################################################################", file=fpout)
        print("TOPCONS2 result file", file=fpout)
        print("Generated from %s at %s"%(base_www_url, date_str), file=fpout)
        print("Total request time: %.1f seconds."%(runtime_in_sec), file=fpout)
        print("##############################################################################", file=fpout)
        cnt = 0
        for line in maplist:
            strs = line.split('\t')
            subfoldername = strs[0]
            length = int(strs[1])
            desp = strs[2]
            seq = strs[3]
            print("Sequence number: %d"%(cnt+1), file=fpout)
            print("Sequence name: %s"%(desp), file=fpout)
            print("Sequence length: %d aa."%(length), file=fpout)
            print("Sequence:\n%s\n\n"%(seq), file=fpout)

            is_TM_cons = False
            is_TM_any = False
            is_nonTM_cons = True
            is_nonTM_any = True
            is_SP_cons = False
            is_SP_any = False

            for i in range(len(methodlist)):
                method = methodlist[i]
                seqid = ""
                seqanno = ""
                top = ""
                if method == "TOPCONS":
                    topfile = "%s/%s/%s/topcons.top"%(outpath_result, subfoldername, "Topcons")
                elif method == "Philius":
                    topfile = "%s/%s/%s/query.top"%(outpath_result, subfoldername, "philius")
                elif method == "SCAMPI":
                    topfile = "%s/%s/%s/query.top"%(outpath_result, subfoldername, method+"_MSA")
                else:
                    topfile = "%s/%s/%s/query.top"%(outpath_result, subfoldername, method)
                if os.path.exists(topfile):
                    (seqid, seqanno, top) = myfunc.ReadSingleFasta(topfile)
                else:
                    top = ""
                if top == "":
                    #top = "***No topology could be produced with this method topfile=%s***"%(topfile)
                    top = "***No topology could be produced with this method***"

                if fpstat != None:
                    if top.find('M') >= 0:
                        is_TM_any = True
                        is_nonTM_any = False
                        if method == "TOPCONS":
                            is_TM_cons = True
                            is_nonTM_cons = False
                    if top.find('S') >= 0:
                        is_SP_any = True
                        if method == "TOPCONS":
                            is_SP_cons = True

                if method == "Homology":
                    showtext_homo = method
                    if seqid != "":
                        showtext_homo = seqid
                    print("%s:\n%s\n\n"%(showtext_homo, top), file=fpout)
                else:
                    print("%s predicted topology:\n%s\n\n"%(method, top), file=fpout)


            if fpstat:
                num_TMPro_cons += is_TM_cons
                num_TMPro_any += is_TM_any
                num_nonTMPro_cons += is_nonTM_cons
                num_nonTMPro_any += is_nonTM_any
                num_SPPro_cons += is_SP_cons
                num_SPPro_any += is_SP_any

            dgfile = "%s/%s/dg.txt"%(outpath_result, subfoldername)
            dg_content = ""
            if os.path.exists(dgfile):
                dg_content = myfunc.ReadFile(dgfile)
            lines = dg_content.split("\n")
            dglines = []
            for line in lines:
                if line and line[0].isdigit():
                    dglines.append(line)
            if len(dglines)>0:
                print("\nPredicted Delta-G-values (kcal/mol) "\
                        "(left column=sequence position; right column=Delta-G)\n", file=fpout)
                print("\n".join(dglines), file=fpout)

            reliability_file = "%s/%s/Topcons/reliability.txt"%(outpath_result, subfoldername)
            reliability = ""
            if os.path.exists(reliability_file):
                reliability = myfunc.ReadFile(reliability_file)
            if reliability != "":
                print("\nPredicted TOPCONS reliability (left "\
                        "column=sequence position; right column=reliability)\n", file=fpout)
                print(reliability, file=fpout)
            print("##############################################################################", file=fpout)
            cnt += 1

        fpout.close()

        if fpstat:
            out_str_list = []
            out_str_list.append("num_TMPro_cons %d"% num_TMPro_cons)
            out_str_list.append("num_TMPro_any %d"% num_TMPro_any)
            out_str_list.append("num_nonTMPro_cons %d"% num_nonTMPro_cons)
            out_str_list.append("num_nonTMPro_any %d"% num_nonTMPro_any)
            out_str_list.append("num_SPPro_cons %d"% num_SPPro_cons)
            out_str_list.append("num_SPPro_any %d"% num_SPPro_any)
            fpstat.write("%s"%("\n".join(out_str_list)))

            fpstat.close()

        rstdir = os.path.realpath("%s/.."%(outpath_result))
        runjob_logfile = "%s/%s"%(rstdir, "runjob.log")
        runjob_errfile = "%s/%s"%(rstdir, "runjob.err")
        finishtagfile = "%s/%s"%(rstdir, "write_result_finish.tag")
        WriteDateTimeTagFile(finishtagfile, runjob_logfile, runjob_errfile)
    except IOError:
        print("Failed to write to file %s"%(outfile))
#}}}

def WriteHTMLHeader(title, fpout):#{{{
    exturl = "http://topcons.net/static"
    print("<HTML>", file=fpout)
    print("<head>", file=fpout)
    print("<title>%s</title>"%(title), file=fpout)
    print("<link rel=\"stylesheet\" href=\"%s/css/jquery.dataTables.css\" type=\"text/css\" />"%(exturl), file=fpout)
    print("<link rel=\"stylesheet\" href=\"%s/css/template_css.css\" type=\"text/css\" />"%(exturl), file=fpout)
    print("<script src=\"%s/js/sorttable.js\"></script>"%(exturl), file=fpout)
    print("<script src=\"%s/js/jquery.js\"></script>"%(exturl), file=fpout) 
    print("<script src=\"%s/js/jquery.dataTables.min.js\"></script>"%(exturl), file=fpout) 
    print("<script>", file=fpout)
    print("$(function(){", file=fpout)
    print("  $(\"#jobtable\").dataTable();", file=fpout)
    print("  })", file=fpout)
    print("</script>", file=fpout)
    print("</head>", file=fpout)
    print("<BODY>", file=fpout)
#}}}
def WriteHTMLTail(fpout):#{{{
    print("</BODY>", file=fpout)
    print("</HTML>", file=fpout)
#}}}
def WriteHTMLTableContent_TOPCONS(tablename, tabletitle, index_table_header,#{{{
        index_table_content_list, fpout):
    """Write the content of the html table for TOPCONS
    """
    print("<a name=\"%s\"></a><h4>%s</h4>"%(tablename,tabletitle), file=fpout)
    print("<table class=\"sortable\" id=\"jobtable\" border=1>", file=fpout)
    print("<thead>", file=fpout)
    print("<tr>", file=fpout)
    for item in index_table_header:
        print("<th>", file=fpout)
        print(item, file=fpout)
        print("</th>", file=fpout)
    print("</tr>", file=fpout)
    print("</thead>", file=fpout)

    print("<tbody>", file=fpout)

    for record in index_table_content_list:
        print("<tr>", file=fpout)
        for i in range(6):
            print("<td>%s</td>"%(record[i]), file=fpout)
        print("<td>", file=fpout)
        print("<a href=\"%s/Topcons/total_image.png\">Fig_all</a>"%(record[6]), file=fpout)
        print("<a href=\"%s/Topcons/topcons.png\">Fig_topcons</a><br>"%(record[6]), file=fpout)
        print("<a href=\"%s/query.result.txt\">Dumped prediction</a><br>"%(record[6]), file=fpout)
        print("<a href=\"%s/dg.txt\">deltaG</a><br>"%(record[6]), file=fpout)
        print("<a href=\"%s/nicetop.html\">Topology view</a><br>"%(record[6]), file=fpout)
        print("</td>", file=fpout)
        print("<td>%s</td>"%(record[7]), file=fpout)
        print("</tr>", file=fpout)

    print("</tbody>", file=fpout)
    print("</table>", file=fpout)
#}}}

@timeit
def WriteHTMLResultTable_TOPCONS(outfile, finished_seq_file):#{{{
    """Write html table for the results
    """
    try:
        fpout = open(outfile, "w")
    except OSError:
        print("Failed to write to file %s at%s"%(outfile,
                sys._getframe().f_code.co_name ), file=sys.stderr)
        return 1

    title="TOPCONS2 predictions"
    WriteHTMLHeader(title, fpout)
    print("<dir id=\"Content\">", file=fpout)
    tablename = 'table1'
    tabletitle = ""
    index_table_header = ["No.", "Length", "numTM",
            "SignalPeptide", "RunTime(s)", "SequenceName", "Prediction", "Source" ]
    index_table_content_list = []
    indexmap_content = myfunc.ReadFile(finished_seq_file).split("\n")
    cnt = 0
    for line in indexmap_content:
        strs = line.split("\t")
        if len(strs)>=7:
            subfolder = strs[0]
            length_str = strs[1]
            numTM_str = strs[2]
            isHasSP = "No"
            if strs[3] == "True":
                isHasSP = "Yes"
            source = strs[4]
            try:
                runtime_in_sec_str = "%.1f"%(float(strs[5]))
            except:
                runtime_in_sec_str = ""
            desp = strs[6]
            rank = "%d"%(cnt+1)
            index_table_content_list.append([rank, length_str, numTM_str,
                isHasSP, runtime_in_sec_str, desp, subfolder, source])
            cnt += 1
    WriteHTMLTableContent_TOPCONS(tablename, tabletitle, index_table_header,
            index_table_content_list, fpout)
    print("</dir>", file=fpout)

    WriteHTMLTail(fpout)
    fpout.close()

    rstdir = os.path.abspath(os.path.dirname(os.path.abspath(outfile))+'/../')
    runjob_logfile = "%s/%s"%(rstdir, "runjob.log")
    runjob_errfile = "%s/%s"%(rstdir, "runjob.err")
    finishtagfile = "%s/%s"%(rstdir, "write_htmlresult_finish.tag")
    WriteDateTimeTagFile(finishtagfile, runjob_logfile, runjob_errfile)
    return 0
#}}}

def ReplaceDescriptionSingleFastaFile(infile, new_desp):#{{{
    """Replace the description line of the fasta file by the new_desp
    """
    if os.path.exists(infile):
        (seqid, seqanno, seq) = myfunc.ReadSingleFasta(infile)
        if seqanno != new_desp:
            myfunc.WriteFile(">%s\n%s\n"%(new_desp, seq), infile)
        return 0
    else:
        sys.stderr.write("infile %s does not exists at %s\n"%(infile, sys._getframe().f_code.co_name))
        return 1
#}}}
def GetLocDef(predfile):#{{{
    """
    Read in LocDef and its corresponding score from the subcons prediction file
    """
    content = ""
    if os.path.exists(predfile):
        content = myfunc.ReadFile(predfile)

    loc_def = None
    loc_def_score = None
    if content != "":
        lines = content.split("\n")
        if len(lines)>=2:
            strs0 = lines[0].split("\t")
            strs1 = lines[1].split("\t")
            strs0 = [x.strip() for x in strs0]
            strs1 = [x.strip() for x in strs1]
            if len(strs0) == len(strs1) and len(strs0) > 2:
                if strs0[1] == "LOC_DEF":
                    loc_def = strs1[1]
                    dt_score = {}
                    for i in range(2, len(strs0)):
                        dt_score[strs0[i]] = strs1[i]
                    if loc_def in dt_score:
                        loc_def_score = dt_score[loc_def]

    return (loc_def, loc_def_score)
#}}}
def datetime_str_to_epoch(date_str):# {{{
    """convert the date_time in string to epoch
    The string of date_time may with or without the zone info
    """
    return dtparser.parse(date_str).strftime("%s")
# }}}
def datetime_str_to_time(date_str):# {{{
    """convert the date_time in string to datetime type
    The string of date_time may with or without the zone info
    """
    strs = date_str.split()
    dt = dtparser.parse(date_str)
    if len(strs) == 2:
        dt = dt.replace(tzinfo=timezone('UTC'))
    return dt
# }}}
def IsFrontEndNode(base_www_url):#{{{
    """
    check if the base_www_url is front-end node
    if base_www_url is ip address, then not the front-end
    otherwise yes
    """
    base_www_url = base_www_url.lstrip("http://").lstrip("https://").split("/")[0]
    if base_www_url == "":
        return False
    elif base_www_url.find("computenode") != -1:
        return False
    else:
        arr =  [x.isdigit() for x in base_www_url.split('.')]
        if all(arr):
            return False
        else:
            return True
#}}}
def GetAverageNewRunTime(finished_seq_file, window=100):#{{{
    """Get average running time of the newrun tasks for the last x number of
sequences
    """
    logger = logging.getLogger(__name__)
    avg_newrun_time = -1.0
    if not os.path.exists(finished_seq_file):
        return avg_newrun_time
    else:
        indexmap_content = myfunc.ReadFile(finished_seq_file).split("\n")
        indexmap_content = indexmap_content[::-1]
        cnt = 0
        sum_run_time = 0.0
        for line in indexmap_content:
            strs = line.split("\t")
            if len(strs)>=7:
                source = strs[4]
                if source == "newrun":
                    try:
                        sum_run_time += float(strs[5])
                        cnt += 1
                    except:
                        logger.debug("bad format in finished_seq_file (%s) with line \"%s\""%(finished_seq_file, line))
                        pass

                if cnt >= window:
                    break

        if cnt > 0:
            avg_newrun_time = sum_run_time/float(cnt)
        return avg_newrun_time


#}}}
def ValidateQuery(request, query, g_params):#{{{
    query['errinfo_br'] = ""
    query['errinfo_content'] = ""
    query['warninfo'] = ""

    has_pasted_seq = False
    has_upload_file = False
    if query['rawseq'].strip() != "":
        has_pasted_seq = True
    if query['seqfile'] != "":
        has_upload_file = True

    if has_pasted_seq and has_upload_file:
        query['errinfo_br'] += "Confused input!"
        query['errinfo_content'] = "You should input your query by either "\
                "paste the sequence in the text area or upload a file."
        return False
    elif not has_pasted_seq and not has_upload_file:
        query['errinfo_br'] += "No input!"
        query['errinfo_content'] = "You should input your query by either "\
                "paste the sequence in the text area or upload a file "
        return False
    elif query['seqfile'] != "":
        try:
            fp = request.FILES['seqfile']
            fp.seek(0,2)
            filesize = fp.tell()
            if filesize > g_params['MAXSIZE_UPLOAD_FILE_IN_BYTE']:
                query['errinfo_br'] += "Size of uploaded file exceeds limit!"
                query['errinfo_content'] += "The file you uploaded exceeds "\
                        "the upper limit %g Mb. Please split your file and "\
                        "upload again."%(g_params['MAXSIZE_UPLOAD_FILE_IN_MB'])
                return False

            fp.seek(0,0)
            content = fp.read()
        except KeyError:
            query['errinfo_br'] += ""
            query['errinfo_content'] += """
            Failed to read uploaded file \"%s\"
            """%(query['seqfile'])
            return False
        query['rawseq'] = content

    query['filtered_seq'] = ValidateSeq(query['rawseq'], query, g_params)
    is_valid = query['isValidSeq']
    return is_valid
#}}}
def ValidateSeq(rawseq, seqinfo, g_params):#{{{
# seq is the chunk of fasta file
# seqinfo is a dictionary
# return (filtered_seq)
    rawseq = re.sub(r'[^\x00-\x7f]',r' ',rawseq) # remove non-ASCII characters
    rawseq = re.sub(r'[\x0b]',r' ',rawseq) # filter invalid characters for XML
    filtered_seq = ""
    # initialization
    for item in ['errinfo_br', 'errinfo', 'errinfo_content', 'warninfo']:
        if item not in seqinfo:
            seqinfo[item] = ""

    seqinfo['isValidSeq'] = True

    seqRecordList = []
    myfunc.ReadFastaFromBuffer(rawseq, seqRecordList, True, 0, 0)
# filter empty sequences and any sequeces shorter than MIN_LEN_SEQ or longer
# than MAX_LEN_SEQ
    newSeqRecordList = []
    li_warn_info = []
    isHasEmptySeq = False
    isHasShortSeq = False
    isHasLongSeq = False
    isHasDNASeq = False
    cnt = 0
    for rd in seqRecordList:
        seq = rd[2].strip()
        seqid = rd[0].strip()
        if len(seq) == 0:
            isHasEmptySeq = 1
            msg = "Empty sequence %s (SeqNo. %d) is removed."%(seqid, cnt+1)
            li_warn_info.append(msg)
        elif len(seq) < g_params['MIN_LEN_SEQ']:
            isHasShortSeq = 1
            msg = "Sequence %s (SeqNo. %d) is removed since its length is < %d."%(seqid, cnt+1, g_params['MIN_LEN_SEQ'])
            li_warn_info.append(msg)
        elif len(seq) > g_params['MAX_LEN_SEQ']:
            isHasLongSeq = True
            msg = "Sequence %s (SeqNo. %d) is removed since its length is > %d."%(seqid, cnt+1, g_params['MAX_LEN_SEQ'])
            li_warn_info.append(msg)
        elif myfunc.IsDNASeq(seq):
            isHasDNASeq = True
            msg = "Sequence %s (SeqNo. %d) is removed since it looks like a DNA sequence."%(seqid, cnt+1)
            li_warn_info.append(msg)
        else:
            newSeqRecordList.append(rd)
        cnt += 1
    seqRecordList = newSeqRecordList

    numseq = len(seqRecordList)

    if numseq < 1:
        seqinfo['errinfo_br'] += "Number of input sequences is 0!\n"
        t_rawseq = rawseq.lstrip()
        if t_rawseq and t_rawseq[0] != '>':
            seqinfo['errinfo_content'] += "Bad input format. The FASTA format should have an annotation line start with '>'.\n"
        if len(li_warn_info) >0:
            seqinfo['errinfo_content'] += "\n".join(li_warn_info) + "\n"
        if not isHasShortSeq and not isHasEmptySeq and not isHasLongSeq and not isHasDNASeq:
            seqinfo['errinfo_content'] += "Please input your sequence in FASTA format.\n"

        seqinfo['isValidSeq'] = False
    elif numseq > g_params['MAX_NUMSEQ_PER_JOB']:
        seqinfo['errinfo_br'] += "Number of input sequences exceeds the maximum (%d)!\n"%(
                g_params['MAX_NUMSEQ_PER_JOB'])
        seqinfo['errinfo_content'] += "Your query has %d sequences. "%(numseq)
        seqinfo['errinfo_content'] += "However, the maximal allowed sequences per job is %d. "%(
                g_params['MAX_NUMSEQ_PER_JOB'])
        seqinfo['errinfo_content'] += "Please split your query into smaller files and submit again.\n"
        seqinfo['isValidSeq'] = False
    else:
        li_badseq_info = []
        if 'isForceRun' in seqinfo and seqinfo['isForceRun'] and numseq > g_params['MAX_NUMSEQ_FOR_FORCE_RUN']:
            seqinfo['errinfo_br'] += "Invalid input!"
            seqinfo['errinfo_content'] += "You have chosen the \"Force Run\" mode. "\
                    "The maximum allowable number of sequences of a job is %d. "\
                    "However, your input has %d sequences."%(g_params['MAX_NUMSEQ_FOR_FORCE_RUN'], numseq)
            seqinfo['isValidSeq'] = False


# checking for bad sequences in the query

    if seqinfo['isValidSeq']:
        for i in range(numseq):
            seq = seqRecordList[i][2].strip()
            anno = seqRecordList[i][1].strip().replace('\t', ' ')
            seqid = seqRecordList[i][0].strip()
            seq = seq.upper()
            seq = re.sub("[\s\n\r\t]", '', seq)
            li1 = [m.start() for m in re.finditer("[^ABCDEFGHIKLMNPQRSTUVWYZX*-]", seq)]
            if len(li1) > 0:
                for j in range(len(li1)):
                    msg = "Bad letter for amino acid in sequence %s (SeqNo. %d) "\
                            "at position %d (letter: '%s')"%(seqid, i+1,
                                    li1[j]+1, seq[li1[j]])
                    li_badseq_info.append(msg)

        if len(li_badseq_info) > 0:
            seqinfo['errinfo_br'] += "There are bad letters for amino acids in your query!\n"
            seqinfo['errinfo_content'] = "\n".join(li_badseq_info) + "\n"
            seqinfo['isValidSeq'] = False

# convert some non-classical letters to the standard amino acid symbols
# Scheme:
#    out of these 26 letters in the alphabet, 
#    B, Z -> X
#    U -> C
#    *, - will be deleted
    if seqinfo['isValidSeq']:
        li_newseq = []
        for i in range(numseq):
            seq = seqRecordList[i][2].strip()
            anno = seqRecordList[i][1].strip()
            seqid = seqRecordList[i][0].strip()
            seq = seq.upper()
            seq = re.sub("[\s\n\r\t]", '', seq)
            anno = anno.replace('\t', ' ') #replace tab by whitespace


            li1 = [m.start() for m in re.finditer("[BZ]", seq)]
            if len(li1) > 0:
                for j in range(len(li1)):
                    msg = "Amino acid in sequence %s (SeqNo. %d) at position %d "\
                            "(letter: '%s') has been replaced by 'X'"%(seqid,
                                    i+1, li1[j]+1, seq[li1[j]])
                    li_warn_info.append(msg)
                seq = re.sub("[BZ]", "X", seq)

            li1 = [m.start() for m in re.finditer("[U]", seq)]
            if len(li1) > 0:
                for j in range(len(li1)):
                    msg = "Amino acid in sequence %s (SeqNo. %d) at position %d "\
                            "(letter: '%s') has been replaced by 'C'"%(seqid,
                                    i+1, li1[j]+1, seq[li1[j]])
                    li_warn_info.append(msg)
                seq = re.sub("[U]", "C", seq)

            li1 = [m.start() for m in re.finditer("[*]", seq)]
            if len(li1) > 0:
                for j in range(len(li1)):
                    msg = "Translational stop in sequence %s (SeqNo. %d) at position %d "\
                            "(letter: '%s') has been deleted"%(seqid,
                                    i+1, li1[j]+1, seq[li1[j]])
                    li_warn_info.append(msg)
                seq = re.sub("[*]", "", seq)

            li1 = [m.start() for m in re.finditer("[-]", seq)]
            if len(li1) > 0:
                for j in range(len(li1)):
                    msg = "Gap in sequence %s (SeqNo. %d) at position %d "\
                            "(letter: '%s') has been deleted"%(seqid,
                                    i+1, li1[j]+1, seq[li1[j]])
                    li_warn_info.append(msg)
                seq = re.sub("[-]", "", seq)

            # check the sequence length again after potential removal of
            # translation stop
            if len(seq) < g_params['MIN_LEN_SEQ']:
                isHasShortSeq = 1
                msg = "Sequence %s (SeqNo. %d) is removed since its length is < %d (after removal of translation stop)."%(seqid, i+1, g_params['MIN_LEN_SEQ'])
                li_warn_info.append(msg)
            else:
                li_newseq.append(">%s\n%s"%(anno, seq))

        filtered_seq = "\n".join(li_newseq) # seq content after validation
        seqinfo['numseq'] = len(li_newseq)
        seqinfo['warninfo'] = "\n".join(li_warn_info) + "\n"

    seqinfo['errinfo'] = seqinfo['errinfo_br'] + seqinfo['errinfo_content']
    return filtered_seq
#}}}
def InsertFinishDateToDB(date_str, md5_key, seq, outdb):# {{{
    """ Insert the finish date to the sqlite3 database
    """
    tbname_content = "data"
    try:
        con = sqlite3.connect(outdb)
    except Exception as e:
        print(("Failed to connect to the database outdb %s"%(outdb)))
    with con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS %s
            (
                md5 TEXT PRIMARY KEY,
                seq TEXT,
                date_finish TEXT
            )"""%(tbname_content))
        cmd =  "INSERT OR REPLACE INTO %s(md5,  seq, date_finish) VALUES('%s', '%s','%s')"%(tbname_content, md5_key, seq, date_str)
        try:
            cur.execute(cmd)
            return 0
        except Exception as e:
            print("Exception %s"%(str(e)), file=sys.stderr)
            return 1

# }}}
def GetInfoFinish_TOPCONS2(outpath_this_seq, origIndex, seqLength, seqAnno, source_result="", runtime=0.0):# {{{
    """Get the list info_finish for the method TOPCONS2"""
    topfile = "%s/%s/topcons.top"%(
            outpath_this_seq, "Topcons")
    top = myfunc.ReadFile(topfile).strip()
    numTM = myfunc.CountTM(top)
    posSP = myfunc.GetSPPosition(top)
    if len(posSP) > 0:
        isHasSP = True
    else:
        isHasSP = False
    date_str = time.strftime(FORMAT_DATETIME)
    info_finish = [ "seq_%d"%origIndex,
            str(seqLength), str(numTM),
            str(isHasSP), source_result, str(runtime),
            seqAnno.replace('\t', ' '), date_str]
    return info_finish
# }}}
def WriteDateTimeTagFile(outfile, logfile, errfile):# {{{
    if not os.path.exists(outfile):
        date_str = time.strftime(FORMAT_DATETIME)
        try:
            myfunc.WriteFile(date_str, outfile)
            msg = "Write tag file %s succeeded"%(outfile)
            myfunc.WriteFile("[%s] %s\n"%(date_str, msg),  logfile, "a", True)
        except Exception as e:
            msg = "Failed to write to file %s with message: \"%s\""%(outfile, str(e))
            myfunc.WriteFile("[%s] %s\n"%(date_str, msg),  errfile, "a", True)
# }}}
def RunCmd(cmd, logfile, errfile, verbose=False):# {{{
    """Input cmd in list
       Run the command and also output message to logs
    """
    begin_time = time.time()

    isCmdSuccess = False
    cmdline = " ".join(cmd)
    date_str = time.strftime(FORMAT_DATETIME)
    rmsg = ""
    try:
        rmsg = subprocess.check_output(cmd, encoding='UTF-8')
        if verbose:
            msg = "workflow: %s"%(cmdline)
            myfunc.WriteFile("[%s] %s\n"%(date_str, msg),  logfile, "a", True)
        isCmdSuccess = True
    except subprocess.CalledProcessError as e:
        msg = "cmdline: %s\nFailed with message \"%s\""%(cmdline, str(e))
        myfunc.WriteFile("[%s] %s\n"%(date_str, msg),  errfile, "a", True)
        isCmdSuccess = False
        pass

    end_time = time.time()
    runtime_in_sec = end_time - begin_time

    return (isCmdSuccess, runtime_in_sec)
# }}}
def SendEmail_TOPCONS2(jobid, base_www_url, finish_status, to_email="", contact_email="", logfile="", errfile=""):# {{{
    """Send notification email to the user for TOPCONS2 web-server"""
    err_msg = ""
    if os.path.exists(errfile):
        err_msg = myfunc.ReadFile(errfile)

    from_email = "info@topcons.net"
    subject = "Your result for TOPCONS2 JOBID=%s"%(jobid)
    if finish_status == "success":
        bodytext = """
Your result is ready at %s/pred/result/%s

Thanks for using TOPCONS2

    """%(base_www_url, jobid)
    elif finish_status == "failed":
        bodytext="""
We are sorry that your job with jobid %s is failed.

Please contact %s if you have any questions.

Attached below is the error message:
%s
        """%(jobid, contact_email, err_msg)
    else:
        bodytext="""
Your result is ready at %s/pred/result/%s

We are sorry that TOPCONS failed to predict some sequences of your job.

Please re-submit the queries that have been failed.

If you have any further questions, please contact %s.

Attached below is the error message:
%s
        """%(base_www_url, jobid, contact_email, err_msg)

    myfunc.WriteFile("Sendmail %s -> %s, %s"% (from_email, to_email, subject), logfile, "a", True)
    rtValue = myfunc.Sendmail(from_email, to_email, subject, bodytext)
    if rtValue != 0:
        date_str = time.strftime(FORMAT_DATETIME)
        msg =  "Sendmail to {} failed with status {}".format(to_email, rtValue)
        myfunc.WriteFile("[%s] %s\n"%(date_str, msg), errfile, "a", True)
        return 1
    else:
        return 0
# }}}
def GetJobCounter(info): #{{{
# get job counter for the client_ip
# get the table from runlog, 
# for queued or running jobs, if source=web and numseq=1, check again the tag file in
# each individual folder, since they are queued locally
    logfile_query = info['divided_logfile_query']
    logfile_finished_jobid = info['divided_logfile_finished_jobid']
    isSuperUser = info['isSuperUser']
    client_ip = info['client_ip']
    maxdaystoshow = info['MAX_DAYS_TO_SHOW']
    path_result = info['path_result']

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
                if not isSuperUser and ip != client_ip:
                    continue

                submit_date_str = strs[0]
                isValidSubmitDate = True
                try:
                    submit_date = datetime_str_to_time(submit_date_str)
                except ValueError:
                    isValidSubmitDate = False

                if not isValidSubmitDate:
                    continue

                diff_date = current_time - submit_date
                if diff_date.days > maxdaystoshow:
                    continue
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

def CleanJobFolder_TOPCONS2(rstdir):# {{{
    """Clean the jobfolder for TOPCONS2 after finishing"""
    flist =[
            "%s/remotequeue_seqindex.txt"%(rstdir),
            "%s/torun_seqindex.txt"%(rstdir)
            ]
    for f in flist:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass
# }}}
def DeleteOldResult(path_result, path_log, logfile, MAX_KEEP_DAYS=180):#{{{
    """Delete jobdirs that are finished > MAX_KEEP_DAYS
    """
    finishedjoblogfile = "%s/finished_job.log"%(path_log)
    finished_job_dict = myfunc.ReadFinishedJobLog(finishedjoblogfile)
    for jobid in finished_job_dict:
        li = finished_job_dict[jobid]
        try:
            finish_date_str = li[8]
        except IndexError:
            finish_date_str = ""
            pass
        if finish_date_str != "":
            isValidFinishDate = True
            try:
                finish_date = datetime_str_to_time(finish_date_str)
            except ValueError:
                isValidFinishDate = False

            if isValidFinishDate:
                current_time = datetime.now(timezone(TZ))
                timeDiff = current_time - finish_date
                if timeDiff.days > MAX_KEEP_DAYS:
                    rstdir = "%s/%s"%(path_result, jobid)
                    date_str = time.strftime(FORMAT_DATETIME)
                    msg = "\tjobid = %s finished %d days ago (>%d days), delete."%(jobid, timeDiff.days, MAX_KEEP_DAYS)
                    myfunc.WriteFile("[%s] "%(date_str)+ msg + "\n", logfile, "a", True)
                    shutil.rmtree(rstdir)
#}}}
def loginfo(msg, outfile):# {{{
    """Write loginfo to outfile, appending current time"""
    date_str = time.strftime(FORMAT_DATETIME)
    myfunc.WriteFile("[%s] %s\n"%(date_str, msg), outfile, "a", True)
# }}}
@timeit
def CleanServerFile(logfile, errfile):#{{{
    """Clean old files on the server"""
# clean tmp files
    msg = "CleanServerFile..."
    date_str = time.strftime(FORMAT_DATETIME)
    myfunc.WriteFile("[%s] %s\n"%(date_str, msg), logfile, "a", True)
    cmd = ["bash", "%s/clean_server_file.sh"%(rundir)]
    RunCmd(cmd, logfile, errfile)
#}}}
@timeit
def CleanCachedResult(logfile, errfile):#{{{
    """Clean outdated cahced results on the server"""
# clean tmp files
    msg = "Clean cached results..."
    date_str = time.strftime(FORMAT_DATETIME)
    myfunc.WriteFile("[%s] %s\n"%(date_str, msg), logfile, "a", True)
    cmd = ["python", "%s/clean_cached_result.py"%(rundir), "-max-keep-day", "480"]
    RunCmd(cmd, logfile, errfile)
#}}}

def ReadRuntimeFromFile(timefile, default_runtime=0.0):# {{{
    """Read runtime from timefile"""
    if os.path.exists(timefile):
        txt = myfunc.ReadFile(timefile).strip()
        ss2 = txt.split(";")
        try:
            runtime = float(ss2[1])
        except:
            runtime = default_runtime
    else:
        runtime = default_runtime
    return runtime
# }}}
def ArchiveLogFile(path_log, threshold_logfilesize=20*1024*1024):# {{{
    """Archive some of the log files if they are too big"""
    gen_logfile = "%s/qd_fe.log"%(path_log)
    gen_errfile = "%s/qd_fe.err"%(path_log)
    flist = [gen_logfile, gen_errfile,
            "%s/restart_qd_fe.cgi.log"%(path_log),
            "%s/debug.log"%(path_log),
            "%s/clean_cached_result.py.log"%(path_log)
            ]

    for f in flist:
        if os.path.exists(f):
            myfunc.ArchiveFile(f, threshold_logfilesize)
# }}}
