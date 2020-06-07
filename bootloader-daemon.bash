#! /bin/bash

cd "$(dirname $0)"

echo "step 1" > ~/Desktop/log.txt
echo "### Downloading .elf file from server ###"
cd Firebase-database/
python3 download-script.py

# if no new .elf is found
if [ $? -eq 1 ]; then
   exit
fi

echo "######"

echo "step 2" >> ~/Desktop/log.txt
echo "### Moving .elf file to parser location ###"
mv file.elf ../ELF-parser/Python-script/
echo "######"

echo "step 3" >> ~/Desktop/log.txt
echo "### Parsing .elf file ###"
cd ../ELF-parser/Python-script/
python3 ELF_Parser.py file.elf
echo "######"

echo "step 4" >> ~/Desktop/log.txt
echo "### Moving parsed files to communicator location ###"
mv DATA_FILE.txt INFO_FILE.txt TEXT_FILE.txt ../../RPI-communicator/bin/
echo "######"

echo "step 5" >> ~/Desktop/log.txt
echo "### Executing communicator program ###"
cd ../../RPI-communicator/bin/
echo  >last-progress.txt
echo  >progress.txt
python3 progress-script.py &
./a
echo "######"

echo "step 6, final" >> ~/Desktop/log.txt

