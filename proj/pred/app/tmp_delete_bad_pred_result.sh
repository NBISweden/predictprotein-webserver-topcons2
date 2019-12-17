#!/bin/bash 

usage="
USAEG: $0 OPTION

OPTION  {action,dryrun}, default: dryrun
"

option=$1

isDryRun=1

if [ "$option" == "action" ];then
    isDryRun=0
fi

exec_cal_md5=/data3/wk/MPTopo/src/cal_fasta_md5.py
rundir=`dirname $0`
rundir=`readlink -f $rundir`

path_result=$rundir/../static/result
path_result=`readlink -f $path_result`
path_cache=$path_result/cache

echo "path_result=$path_result"

cd $path_result
rstdirlist=$(find . -maxdepth 1 -type d   -name "rst_*" )

for rstdir in $rstdirlist; do
    rstdir=`basename $rstdir`
    seqfolderlist=$(find $rstdir/$rstdir -maxdepth 3 -name "seq_*" -type d )
    for seqfolder in $seqfolderlist; do
        topfile=$seqfolder/Topcons/topcons.top
        fafile=$seqfolder/seq.fa
        if [  ! -s $topfile ];then
            echo "rm -rf $seqfolder"
            if [ $isDryRun -eq 0 ];then
                rm -rf $seqfolder
            fi
            md5key=`awk '/^[^>]/ {printf ("%s", $1)}' $fafile | md5sum | awk '{print $1}'`
            sizekey=${#md5key}
            if [ $sizekey -gt 2 ];then
                cachefile=$path_cache/${md5key:0:2}/$md5key.zip
                echo "rm -f $cachefile"
                if [ $isDryRun -eq 0 ];then
                    rm -f $cachefile
                fi
            fi
        fi
    done
done


