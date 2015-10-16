import socket
import sys

def server(ip="localhost", port=8000):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((ip, port))
    serversocket.listen(5)

    while 1:
        client, address = serversocket.accept()
        print 'client accepted, address: {}:{}'.format(client, address)


def client(ip, port):
    s = socket.socket()
    s.connect((ip, port))
    print(s.recv(1024))
