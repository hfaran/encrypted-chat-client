import socket
from abc import abstractproperty
from abc import abstractmethod


class Sock(object):
    """Base class for Client and Server"""

    BUFSIZE = 4096

    @abstractproperty
    def conn(self):
        raise NotImplementedError

    def send(self, msg):
        self.conn.send(msg)

    def recv(self):
        return self.conn.recv(self.BUFSIZE)

    @abstractmethod
    def close(self):
        raise NotImplementedError


class Client(Sock):
    """Client

    :param str remote_ip: Remote IP
    :param int remote_port: Remote Port
    """
    def __init__(self, remote_ip, remote_port):
        self._sock = socket.socket()
        self._sock.connect((remote_ip, remote_port))

    @property
    def conn(self):
        return self._sock

    def close(self):
        self._sock.close()


class Server(Sock):
    def __init__(self, ip, port):
        self.sock = socket.socket()
        self.sock.bind((ip, port))
        self.sock.listen(5)
        self._conn, (self.client_ip, self.client_port) = self.sock.accept()

    @property
    def conn(self):
        return self._conn

    def close(self):
        self.conn.close()
        self.sock.close()
