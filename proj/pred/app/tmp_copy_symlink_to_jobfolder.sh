#!/bin/bash

# Description: copy the data in cache to this folder, so that seq_origIndex is
# not a symlink but the folder contains the actual data

filelist=$*
for file in $filelist;do
    if [ ! -L $file ];then
        continue
    fi
    rm -f $file
    realpath=$(readlink  $file )
    rsync -arz  $realpath/ $file/
    chown apache:apache -R $file
done
