#! /bin/bash


cd ~/Desktop/Firebase-database

python3 download-script.py

cd ~/Desktop/ELF-parser/Python-script/

mv bootloader-dummy-app.elf ~/Desktop/ELF-parser/Python-script/

cd ~/Desktop/ELF-parser/Python-script/

python3 ELF_Parser.py

mv DATA_FILE.txt INFO_FILE.txt TEXT_FILE.txt ~/Desktop/RPI-communicator/

cd ~/Desktop/RPI-communicator/

./a

