from abc import abstractproperty
from abc import abstractmethod

from ect.message import Client
from ect.message import Server


class ChatClientBase(object):

    @abstractproperty
    def Ks(self):
        """Session key"""
        raise NotImplementedError

    @property
    def authenticated(self):
        """Determine if we are authenticated by checking for a session key"""
        return self.Ks is not None

    @abstractmethod
    def send(self, message):
        """Send a message to the remote"""
        raise NotImplementedError

    @abstractmethod
    def recv_loop(self):
        """This method should be invoked as a thread and be continually
        listening for and receiving messages
        """
        raise NotImplementedError


class ChatClientClient(ChatClientBase):
    """Alice"""
    def __init__(self, remote_ip, remote_port, local_ip="0.0.0.0",
                 local_port=8050):
        self.client = Client(remote_ip, remote_port)
        self.server = Server(local_ip, local_port)
        self._kes = self.KEY_EXCHANGE_STATES[-1]  # key exchange state
        self._session_key = None

    KEY_EXCHANGE_STATES = {
        -1: None,
        0: "PUBKEY_EXCHANGE",
        1: "VERIFY_REMOTE",
        2: "IDENTIFY_SELF_TO_REMOTE"
    }

    @property
    def Ks(self):
        return self._session_key

    def mutauth_step(self, reset=False):
        """This method steps through mutual authentication using Diffie-Helman

        Each call to this method will perform one step out of the
         total steps necessary for authentication.

        :param bool reset: If this is set, we reset back to step -1
        """
        if reset:
            self._kes = self.KEY_EXCHANGE_STATES[-1]
            return

        if self._kes == self.KEY_EXCHANGE_STATES[-1]:
            # Send our public key (Ra)
            self._Ra = 4  # TODO
            self.client.send(self._Ra)  # TODO
            self._kes = self.KEY_EXCHANGE_STATES[0]
        elif self._kes == self.KEY_EXCHANGE_STATES[0]:
            # Get response: RB, E("Bob", RA, gb mod p, KAB)
            resp = self.server.recv()
            # TODO do things here to verify responses
            # ...
            # Once verified, we can assign the session key and consider
            #  ourselves authenticated
            self._session_key = "something to do with {}".format(resp)
            self._kes = self.KEY_EXCHANGE_STATES[1]
        elif self._kes == self.KEY_EXCHANGE_STATES[1]:
            # Send E("Alice", RB, ga mod p, KAB)
            self.client.send("something_else")
            self._kes = self.KEY_EXCHANGE_STATES[2]
        elif self._kes == self.KEY_EXCHANGE_STATES[2]:
            raise StopIteration("Authentication completed successfully.")


class ChatClientServer(ChatClientBase):
    """Bob"""
    def __init__(self, remote_ip, remote_port, local_ip="0.0.0.0",
                 local_port=8050):
        # Start server first, then client (opposite order from ChatClientClient
        self.server = Server(local_ip, local_port)
        self.client = Client(remote_ip, remote_port)

    # TODO implement this class in similar manner as the above
    #  ChatClientClient class (but as a "server" or "Bob" instead
