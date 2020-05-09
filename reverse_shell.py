#!/usr/bin/python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.0.94",54321))
sock.close()
