#!/bin/bash

# Description: copy the data in cache to this folder, so that seq_origIndex is
# not a symlink but the folder contains the actual data
platform_info=`python -mplatform |  tr '[:upper:]' '[:lower:]'`
platform=
case $platform_info in 
    *centos*)platform=centos;;
    *redhat*) platform=redhat;;
    *ubuntu*|*debian*)platform=ubuntu;;
    *)platform=other;;
esac


case $platform in 
    centos|redhat) user=apache;group=apache;;
    ubuntu) user=www-data;group=www-data;;
    other)echo Unrecognized plat form $platform_info; exit 1;;
esac

filelist=$*

for file in $filelist;do
    if [ ! -L $file ];then
        continue
    fi
    echo $file
    mv  $file $file.tmp
    realpath=$(readlink  -f $file.tmp )
    rsync -arz  $realpath/ $file/
    chown $user:$group -R $file
    rm -f $file.tmp
done
