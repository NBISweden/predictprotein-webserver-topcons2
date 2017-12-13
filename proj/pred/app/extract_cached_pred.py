#!/usr/bin/env python
# -- python2.7+ --

import os
import sys
import myfunc
import argparse
import hashlib


def OutputRecord(seqnumber, seqid, description, seq, fpout):# {{{
    md5_key = hashlib.md5(seq).hexdigest()
    subfoldername = md5_key[:2]
    cachedir = "%s/%s/%s"%(g_params['path_cache'], subfoldername, md5_key)
    if os.path.exists(cachedir):
        resultfile = "%s/query.result.txt"%(cachedir)
        if os.path.exists(resultfile):
            buff = myfunc.ReadFile(resultfile)
            lines = buff.split("\n")
            numLine = len(lines)
            i = 0
            top_topcons = ""
            top_octopus = ""
            top_philius = ""
            top_polyphobius = ""
            top_scampi = ""
            top_spoctopus = ""
            dg = {}

            while i < numLine:
                if lines[i].find("TOPCONS predicted topology:") == 0:
                    top_topcons = lines[i+1].strip()
                    i += 2
                elif lines[i].find("OCTOPUS predicted topology:") == 0:
                    top_octopus = lines[i+1].strip()
                    i += 2
                elif lines[i].find("Philius predicted topology:") == 0:
                    top_philius = lines[i+1].strip()
                    i += 2
                elif lines[i].find("PolyPhobius predicted topology:") == 0:
                    top_polyphobius = lines[i+1].strip()
                    i += 2
                elif lines[i].find("SCAMPI predicted topology:") == 0:
                    top_scampi = lines[i+1].strip()
                    i += 2
                elif lines[i].find("SPOCTOPUS predicted topology:") == 0:
                    top_spoctopus = lines[i+1].strip()
                    i += 2
                elif lines[i].find("Predicted Delta-G-values") == 0:
                    if g_params['isOutputDG'] == "yes":
                        j = i+1
                        while j < numLine:
                            items = lines[j].split()
                            if len(items) == 2 and items[0].isdigit():
                                dg[int(items[0])] = float(items[1])
                            j += 1

                    break
                else:
                    i += 1
            seqlength = len(seq)

            fpout.write("SeqNo: %d\n"%(seqnumber))
            fpout.write("SeqLength: %d\n"%(seqlength))
            fpout.write("SeqName: %s\n"%(description))
            fpout.write("%-13s %s\n"%("Seq:", seq))
            fpout.write("%-13s %s\n"%("TOPCONS2:", top_topcons))
            fpout.write("%-13s %s\n"%("OCTOPUS:", top_octopus))
            fpout.write("%-13s %s\n"%("Philius:", top_philius))
            fpout.write("%-13s %s\n"%("PolyPhobius:", top_polyphobius))
            fpout.write("%-13s %s\n"%("SCAMPI:", top_scampi))
            fpout.write("%-13s %s\n"%("SPOCTOPUS:", top_spoctopus))
            if g_params['isOutputDG'] == "yes":
                fpout.write("DeltaG: %s\n"%(str(dg)))

            fpout.write("\n")

            return 0
    else:
        print >> sys.stderr, "record not found for %s"%(seqid)
        return 1

# }}}

def main(args, g_params):
    parser = argparse.ArgumentParser(
            description='Extract cached result of TOPCONS2 given a seq file',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''\
Created 2017-12-13, updated 2017-12-13, Nanjiang Shu

Examples:
''')
    parser.add_argument('seqfile', metavar='SEQFILE',
            help='Specify the input amino acid sequence file in FASTA format')
    parser.add_argument('-cache', '--cache', metavar='DIR', dest='path_cache',
            help='Specify the directory where the cached results are (default: %s)'%(g_params['path_cache']))
    parser.add_argument('-o', '--outfile', metavar='FILE', dest='outfile', 
            help='Specify the output file')
    parser.add_argument('-outdg','--outdg', action='store', dest='isOutputDG', default='no',
            choices=['yes', 'no'], help='Whether output the DeltaG (default = no)' )
    parser.add_argument('-debug', '--debug', action='store_true', default=False,  dest='isDEBUG', 
            help='Output debug info')


    args = parser.parse_args()

    g_params['DEBUG'] = args.isDEBUG
    seqfile = os.path.abspath(args.seqfile)
    g_params['isOutputDG'] = args.isOutputDG
    if args.path_cache!= None:
        g_params['path_cache'] = os.path.abspath(args.path_cache)
    if args.outfile != None:
        outfile = os.path.abspath(args.outfile)
    else:
        outfile = ""

    fpout = myfunc.myopen(outfile, sys.stdout, "w", False)


    hdl = myfunc.ReadFastaByBlock(seqfile)
    if hdl.failure:
        sys.exit(1)

    recordList = hdl.readseq()
    cnt=0
    while  recordList != None:
        for record in recordList:
            description = record.description
            seq = record.seq
            seqid = record.seqid
            if OutputRecord(cnt+1, seqid, description, seq, fpout) == 0:
                cnt += 1
        recordList = hdl.readseq()
    hdl.close()

    myfunc.myclose(fpout)

def InitGlobalParameter():#{{{
    g_params = {}
    g_params['path_cache'] = "/var/www/html/topcons2/proj/pred/static/result/cache/"
    return g_params
#}}}

if __name__=="__main__":
    g_params = InitGlobalParameter()
    sys.exit(main(sys.argv, g_params))
