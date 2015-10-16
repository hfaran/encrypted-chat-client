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

    def mutual_authentication(self):
        """Coroutine that handles the mutual authentication process

        Whenever there is a `yield <object>` in the coroutine, you
         should use `next(mutauth)` in the calling code, where `mutauth`
         is an instance of the coroutine.
         Whenever there is a `resp = yield` in a coroutine, the calling
         code should send a value using `mutauth.send(resp)`
        """
        # Send our public key (Ra)
        Ra = 4  # TODO
        yield Ra

        # Get response: RB, E("Bob", RA, gb mod p, KAB)
        resp = yield
        # TODO do things here to verify responses

        # Once verified, we can assign the session key and consider
        #  ourselves authenticated
        self._session_key = "something"

        # Send E("Alice", RB, ga mod p, KAB)
        yield "something_else"

    def mutauth_step(self, messsage=None):
        """This method steps through the mutual_authentication coroutine
        by keeping state using self._kes being one of the four key exchange
        states
        """
        if self._kes == self.KEY_EXCHANGE_STATES[-1]:
            self._muauth = self.mutual_authentication()
            res = next(self._muauth)
            self._kes = self.KEY_EXCHANGE_STATES[0]
            return res
        elif self._kes == self.KEY_EXCHANGE_STATES[0]:
            self._muauth.send(messsage)
            self._kes = self.KEY_EXCHANGE_STATES[1]
        elif self._kes == self.KEY_EXCHANGE_STATES[1]:
            res = next(self._muauth)
            self._kes = self.KEY_EXCHANGE_STATES[2]
            return res
        elif self._kes == self.KEY_EXCHANGE_STATES[2]:
            del self._muauth
            self._kes = self.KEY_EXCHANGE_STATES[-1]


class ChatClientServer(ChatClientBase):
    """Bob"""
    def __init__(self, remote_ip, remote_port, local_ip="0.0.0.0",
                 local_port=8050):
        # Start server first, then client (opposite order from ChatClientClient
        self.server = Server(local_ip, local_port)
        self.client = Client(remote_ip, remote_port)

    # TODO implement this class in similar manner as the above
    #  ChatClientClient class (but as a "server" or "Bob" instead
