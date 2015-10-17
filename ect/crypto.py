import os

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.backends import default_backend


BACKEND = default_backend()
BLOCK_SIZE = 32  # bytes
TO_BITS = 8  # multiplication factor to bits from bytes

# Encryption technique recommendations taken from Colin Percival's
# Cryptographic Right Answers.
# http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html
# In addition to advice from the documentation of the Python cryptography
#  package: https://cryptography.io/en/latest

def encrypt(key, message):
    """Encrypt ``message`` with ``key``

    * A cipher is created along with a random nonce.
    * The text is encrypted with the key using AES with CTR.
    * Using HMAC, a MAC is calculated for the ciphertext with a key derived
    from the ``key``.
    * The ciphertext is composed of the encrypted message, the MAC, and the
    nonce

    :type key: str
    :type message: str
    :rtype: str
    """
    # Create encryptor
    cipher, nonce = create_cipher(key)
    encryptor = cipher.encryptor()
    
    # Encrypt message
    ct = encryptor.update(message) + encryptor.finalize()
    
    # Calculate HMAC following Encrypt-then-MAC way
    mac_key = derive_new_key(key)
    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=BACKEND)
    h.update(ct + nonce)
    mac = h.finalize()
    ct += nonce + mac
    return ct


def decrypt(key, ct):
    """Decrypts ciphertext ``ct`` with ``key``"""
    # Decompose the ciphertext
    ct, nonce, mac = ct[:-BLOCK_SIZE*2], ct[-BLOCK_SIZE*2:-BLOCK_SIZE], \
                     ct[-BLOCK_SIZE:]
    
    # Check the MAC
    mac_key = derive_new_key(key)
    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=BACKEND)
    h.update(ct + nonce)
    h.verify(mac)
    # Create the cipher with the extracted nonce
    cipher, _nonce = create_cipher(key, nonce=nonce)
    assert _nonce == nonce
    # Decrypt the plaintext
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    # Return the verified plaintext
    return pt


def create_cipher(key, nonce=None):
    """Creates and returns an AES Cipher with the given key in CTR mode
    with the given nonce; if no nonce is provided generates a new nonce

    :param str key: Key
    :param str nonce: Nonce
    :rtype: tuple
    :returns: (Cipher, nonce)
    """
    # Generate a random nonce of BLOCK_SIZE
    nonce = os.urandom(BLOCK_SIZE) if nonce is None else nonce
    # Create an AES primitive of BLOCK_SIZE (256-bit in this case)
    a = algorithms.AES(key)
    a.block_size = BLOCK_SIZE * TO_BITS
    # Create a Cipher using the AES primitive and CTR mode with the nonce
    cipher = Cipher(a, modes.CTR(nonce), backend=BACKEND)
    return cipher, nonce


# MAC should not use the same key as the encryption
def derive_new_key(key):
    hkdf = HKDFExpand(algorithm=hashes.SHA256(), length=BLOCK_SIZE,
                      info=None, backend=BACKEND)
    return hkdf.derive(key)
