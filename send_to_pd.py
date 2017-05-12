import os
import socket

def send2port(message=''):
    os.system("echo '" + message + ";' | nc localhost 3000")



def send2port_socket(data):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 3001
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))

    #s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)
    conn.send(data)
    conn.close()
