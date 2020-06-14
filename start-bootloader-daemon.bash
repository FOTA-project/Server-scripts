#! /bin/bash

cd "$(dirname $0)"
python3 bootloader-daemon.py &
echo Started bootloader daemon, exiting... >>"bootloader-daemon-log.txt"
exit
