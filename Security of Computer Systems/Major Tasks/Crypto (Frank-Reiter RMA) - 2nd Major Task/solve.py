import random
import base64
import os
import wannacry
import json

from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse as invert
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

# TO RUN YOU NEED:
# a) captures.json - with outcoming udp connections to 35.205.64.152 (ip.dst == 35.205.64.152 and udp)
# b) pub.pem - with Public Key of encrypting script
# c) decryptMe - directory with encrypted files (or other name but you have to change global variable)
# d) wannacry.py - script with Decoder to import decoding class

nameOfEncryptedDirectory = "decryptMe"

# beginof: fetch captures to python readable form
with open('captures.json', 'r') as f:
	captures_list = json.loads(f.read())

captures = list()
for counter, capture in enumerate(captures_list):
	string_with_space_separated_bytes = " ".join(capture['_source']['layers']['data']['data.data'].split(':'))
	a_very_true_bytearray = bytearray.fromhex(string_with_space_separated_bytes)
	captures.append((counter, a_very_true_bytearray))
# endof:   fetch captures to python readable form

# beginof: fetch public key and its digit
with open('pub.pem', 'r') as f:
        rsa = RSA.importKey(f.read())
n = rsa.n
# endof:   fetch public key and its digit

def franklin_reiter_related_message_attack(e, n, c1, c2, a, b):
    assert e == 3 and b != 0
    frac = b * (c2 + 2*pow(a,3)*c1 - pow(b,3))
    denom = a * (c2 - pow(a,3)*c1 + 2*pow(b,3))
    m = (frac * invert(denom, n)) % n
    return m

# beginof: fetch keys
decoding_things = []

previous_index, previous_msg = captures[0]
for index, msg in captures[1:]:
	m_3 = bytes_to_long(base64.b64decode(previous_msg))
	m_31 = bytes_to_long(base64.b64decode(msg))

	m = franklin_reiter_related_message_attack(3, n, m_3, m_31, 1, 1)
	m_enc = base64.b64encode(rsa.encrypt(long_to_bytes(m), 0)[0])
	m_digest = SHA256.new(m_enc).digest()
	m_dig = base64.b64encode(SHA256.new(long_to_bytes(m)).digest())

	decoding_things.append(("%064x" % bytes_to_long(m_digest), m_dig))
	previous_index = index
	previous_msg = msg

# do the last key separately
last_index, last_msg = captures[-1]
_, before_last_index = captures[-2]
m_3 = bytes_to_long(base64.b64decode(last_msg))
m_31 = bytes_to_long(base64.b64decode(before_last_index))
m = franklin_reiter_related_message_attack(3, n, m_3, m_31, 1, -1)
m_enc = base64.b64encode(rsa.encrypt(long_to_bytes(m), 0)[0])
m_digest = SHA256.new(m_enc).digest()
m_dig = base64.b64encode(SHA256.new(long_to_bytes(m)).digest())
decoding_things.append(("%x" % bytes_to_long(m_digest), m_dig))
# endof: fetch keys

# path to directory with encoded files - i use decrypt me
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), nameOfEncryptedDirectory)

# fire up decrypter
dec = wannacry.Decrypter()
dec.process(path, decoding_things)
