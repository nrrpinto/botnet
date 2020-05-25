# README #

Please see below how to set it up.

### What is this repository for? ###

* This is a POC of a botnet programmed in Python3. I developed this following the steps of the UDEMY course "Coding Botnet Backdoor in Python for Ethical Hacking" by Aleksa Tamburkovski. While throught the training course video the instructions were in python2, I followed it but implementing it in python3. My version has some little differences from the course version, like additional persistence, different way to present the messages and menus, small difference on how to manage the reliable data transfer.
* Version 0.1
* [Learn Markdown](https://www.udemy.com/course/coding-botnet-backdoor-in-python-for-ethical-hacking/)

### How do I get set up? ###

* Dependencies

    socket, subprocess, json, sys, os, base64, shutil, time, requests, mss, threading

* Compile the bot

    c:\Python38\Scripts\pyinstaller --onefile --noconsole reverse_shell.py

* Configuration threaded.py:

    **HOST** -> Set the local IP of the server botnet [required]

    **PORT** -> define PORT of the server to receive connections [required]

* Configuration reverse_shell.py:

    **HOST** -> define IP address of the server [required]

    **PORT** -> define PORT of the server [required]

    **pers_loc** -> define persistence [optional]

    **keylogger_path** -> define keylogger file path [options]

    **persist_run** -> Implements persistence through RUN registry key - User Permissions

    **persist_srv** -> Implements persistence through Services registry key - NT Authority/System permissions

    **persist_stu** -> Implements persistence through Start Up user folder - User permissions

* Executing

  * Start the server:

    $ ./Threaded.py

  * Start the bots:

    Double click on the bot

### Who do I talk to? ###

* Repo owner or admin

  f4d0
