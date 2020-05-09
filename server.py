#!/usr/bin/python

import socket
from termcolor import color

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("192.168.0.94",54321))
s.listen(5) # how many connections - 5

print(colored("[+] Listening for Incoming Connections")

target, ip = s.accept()
print(colored("[+] Connection Established From: %s" % str(ip)))
s.close()
