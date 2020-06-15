#! /bin/bash

cd "$(dirname $0)"

while [ 1 ]
do
   python3 bootloader-daemon.py 1>>"bootloader-daemon-log.txt" 2>>"bootloader-daemon-log.txt"
   sleep 1
done

echo Exiting bootloader daemon, exiting... >>"bootloader-daemon-log.txt"

exit
