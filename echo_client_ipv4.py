#!/usr/bin/python
import socket

HOST = '192.168.0.94'
PORT = 54321
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        data = input("Insert something to send: ")
        s.sendall(data.encode('UTF-8'))
        data = s.recv(1024)
        print('Received from echo server: ', repr(data.decode('UTF-8')))
