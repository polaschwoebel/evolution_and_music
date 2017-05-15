import os
import socket

def send2port(message=''):
    os.system("echo '" + message + ";' | nc localhost 3000")



def send2port_socket(data):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 3000
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))

    #s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)
    conn.send(data + ';')
    conn.close()


def send2port_socket_other(data):
    HOST = '127.0.0.1'    # The remote host
    PORT = 3000              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall('2 3 4 5 6 7 7 7 7 10'.encode())
