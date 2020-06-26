# Folder structure

```
~/Desktop/bootloader-daemon      <folder>
|
|
|-- a                            <file>
|-- ELF_Parser.py                <file>
|-- start-bootloader-daemon.bash <file>
|-- bootloader-daemon.py         <file>
```


# How to add the script as a startup daemon 

```bash
crontab -e

@reboot ~/Desktop/bootloader-daemon/start-bootloader-daemon.bash
```
