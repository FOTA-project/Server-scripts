#! /bin/bash

cd "$(dirname $0)"

# source: https://www.raspberrypi.org/forums/viewtopic.php?t=238070
export DISPLAY=":0"

while [ 1 ]
do
   python3 bootloader-daemon.py 1>>"bootloader-daemon-log.txt" 2>>"bootloader-daemon-log.txt"
   sleep 1
done

echo Exiting bootloader daemon, exiting... >>"bootloader-daemon-log.txt"

exit
