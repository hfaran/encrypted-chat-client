import socket
import sys

def server(port) :
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), port))
    serversocket.listen(5)

    while 1:
        client, address = s.accept()
        print 'client accepted, address: '
