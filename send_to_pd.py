import os

def send2port(message=''):
    os.system("echo '" + message + ";' | nc localhost 3000")
