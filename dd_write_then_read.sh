#!/bin/bash
# Simple workload to write a file to /tmp using dd, sleep for 2 seconds, then
# read file using dd.  The file cache is turned off (oflag/iflag=direct) in
# order to see the raw disk performance.

[ "$#" -ne "1" ] && echo USAGE: $0 BLOCK_SIZE && exit 1

BLOCK_SIZE=$1

I=0
mkdir -p /tmp/workload_monitor
OUT_FN=/tmp/workload_monitor/dd_file.$(date +"%Y%m%d-%H%M%S")

# Write
dd if=/dev/zero of=$OUT_FN BLOCK_SIZE=$BLOCK_SIZE count=1024 oflag=direct

# Pause
sleep 2

# Read
dd if=$OUT_FN of=/dev/null BLOCK_SIZE=$BLOCK_SIZE iflag=direct

# clean up
rm $OUT_FN
