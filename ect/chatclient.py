from abc import abstractproperty
from abc import abstractmethod

from message import Client
from message import Server

import crypto
import os

class ChatClientBase(object):
   
    _g = 3 # TODO
    _p = 35791 #TODO
    _shared_key = None

    @abstractproperty
    def Ks(self):
        """Session key"""
        raise NotImplementedError

    # GUI should call this fucntion to set the shared key set by TA
    def set_shared_key(self, key=None):
        self._shared_key = key
    
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

    def extract_auth_msg_parts(self, m):
        ident, nonce, public_key = m[:crypto.BLOCK_SIZE], \
                                   m[crypto.BLOCK_SIZE:crypto.BLOCK_SIZE*2], \
                                   m[crypto.BLOCK_SIZE*2:]
        return ident, nonce, public_key 


class ChatClientClient(ChatClientBase):
    """Alice"""
    def __init__(self, remote_ip, remote_port, local_ip="0.0.0.0",
                 local_port=8050):
        self.client = Client(remote_ip, remote_port)
        self.server = Server(local_ip, local_port)
        self._mutau_state = self.MUTUAL_AUTH_STATES[-1]  # key exchange state
        self._session_key = None
        self._shared_key = None
        self._secret_value = 1357 # TODO

    MUTUAL_AUTH_STATES = {
        -1: None,
        0: "NOTIFY_REMOTE",
        1: "VERIFY_REMOTE",
        2: "IDENTIFY_SELF_TO_REMOTE"
    }


    @property
    def Ks(self):
        return self._session_key

    def mutauth_step(self, reset=False):
        """This method steps through mutual authentication 
            and key exchange using Diffie-Helman

        Each call to this method will perform one step out of the
         total steps necessary for authenticationr

        :param bool reset: If this is set, we reset back to step -1
        """
        if reset or self._shared_key is None:
            self._mutau_state = self.MUTUAL_AUTH_STATES[-1]
            return

        if self._mutau_state == self.MUTUAL_AUTH_STATES[-1]:
            # Send our public key (Ra)
            self._Ra = os.urandom(crypto.BLOCK_SIZE)  # TODO
            print "ra sent:", self._Ra

            self.client.send(self._Ra)  # TODO
            self._mutau_state = self.MUTUAL_AUTH_STATES[0]
            print "step1 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[0]:
            # Get response: RB, E("Bob", RA, gb mod p, KAB)
            resp = self.server.recv()
            # TODO do things here to verify responses
            # ...
            # Once verified, we can assign the session key and consider
            #  ourselves authenticated

            self._rb = resp[:crypto.BLOCK_SIZE]
            ct = resp[crypto.BLOCK_SIZE:]
            pt = crypto.decrypt(self._shared_key, ct)
            print "rb received:", self._rb
            print "ct received:", ct
            print "pt from ct:", pt

            # what's the size of identifier, ra, and gb mod p? are they all fixed
            identifier, ra, gb_mod_p = self.extract_auth_msg_parts(pt)
            print "identifier:", identifier
            print "ra", ra
            print "gb_mod_p", gb_mod_p

            if self._Ra != ra:
                pass # TODO: do something it's Trudy

            # TODO check if correct
            self._session_key = pow(long(gb_mod_p), self._secret_value) % self._p
            self._mutau_state = self.MUTUAL_AUTH_STATES[1]
            print "step2 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[1]:
            # Send E("Alice", RB, ga mod p, KAB)
            identifier = os.urandom(crypto.BLOCK_SIZE)
            ga_mod_p = pow(self._g, self._secret_value) % self._p
            pt = identifier + self._rb + str(ga_mod_p)
            ct = crypto.encrypt(self._shared_key, pt) 
            self.client.send(ct)
            self._mutau_state = self.MUTUAL_AUTH_STATES[2]
            print "step3 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[2]:
            raise StopIteration("Authentication completed successfully.")


class ChatClientServer(ChatClientBase):
    """Bob"""
    
    MUTUAL_AUTH_STATES = {
        -1: None,
        0: "WAIT",
        1: "IDENTIFY_SELF_TO_REMOTE",
        2: "VERIFY_REMOTE"
    }

    def __init__(self, remote_ip, remote_port, local_ip="0.0.0.0",
                 local_port=8051):
        # Start server first, then client (opposite order from ChatClientClient
        self.server = Server(local_ip, local_port)
        self.client = Client(remote_ip, remote_port)
        self._mutau_state = self.MUTUAL_AUTH_STATES[-1]  # key exchange state
        self._secret_value = 1357 # TODO

    def mutauth_step(self, reset=False):
        # TODO implement this class in similar manner as the above
        #  ChatClientClient class (but as a "server" or "Bob" instead
        if reset or self._shared_key is None:
            self._mutau_state = self.MUTUAL_AUTH_STATES[-1]
            return

        if self._mutau_state == self.MUTUAL_AUTH_STATES[-1]:
            # Receive client's nonce
            self._Ra = self.server.recv()
            print "ra received:", self._Ra
            self._mutau_state = self.MUTUAL_AUTH_STATES[0]
            print "step1 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[0]:
            # Send response: RB, E("Bob", RA, gb mod p, KAB)
            self._Rb = os.urandom(crypto.BLOCK_SIZE)  # TODO
            identifier = os.urandom(crypto.BLOCK_SIZE) # TODO
            gb_mod_p = pow(self._g, self._secret_value) % self._p
            pt = identifier + self._Ra + str(gb_mod_p)
            ct = crypto.encrypt(self._shared_key, pt)
            msg = self._Rb + ct
            self.client.send(msg)
            print "Sending data:"
            print "identifier", identifier
            print "ra", self._Ra
            print "rb", self._Rb
            print "gb_mod_p", gb_mod_p

            print "pt", pt
            print "ct", ct
            print "msg", msg

            self._mutau_state = self.MUTUAL_AUTH_STATES[1]
            print "step2 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[1]:
            # Receive E("Alice", RB, ga mod p, KAB)
            ct = self.server.recv()
            pt = crypto.decrypt(self._shared_key, ct)
            print "ct received:", ct
            print "pt from ct:", pt
            
            identifier, rb, ga_mod_p = self.extract_auth_msg_parts(pt)
            print "identifier:", identifier, "rb", rb, "ga_mod_p", ga_mod_p
            
            if self._Rb != rb:
                pass # TODO: do something it's Trudy

            # TODO check if correct
            self._session_key = pow(long(ga_mod_p), self._secret_value) % self._p
            self._mutau_state = self.MUTUAL_AUTH_STATES[2]
            print "step3 done"
        elif self._mutau_state == self.MUTUAL_AUTH_STATES[2]:
            raise StopIteration("Authentication completed successfully.")
