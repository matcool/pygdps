from base64 import b64encode, b64decode
import itertools

class InvalidXORKey(Exception): pass

GJP_KEY = '37526'

def decode(string: str, key: str) -> str:
    if not key.isnumeric():
        raise InvalidXORKey('Invalid XOR key')
    key = key.encode('ascii')
    return bytes(
        c ^ k for c, k in zip(b64decode(string), itertools.cycle(key))
    ).decode()

def encode(string: str, key: str) -> str:
    if not key.isnumeric():
        raise InvalidXORKey('Invalid XOR key')
    key = key.encode('ascii')
    return b64encode(bytes(
        ord(c) ^ k for c, k in zip(string, itertools.cycle(key))
    )).decode()