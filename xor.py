from base64 import b64encode, b64decode

class InvalidXORKey(Exception): pass

GJP_KEY = '37526'

def decode(string: str, key: str) -> str:
    if not key.isnumeric():
        raise InvalidXORKey('Invalid XOR key')
    return ''.join(
        chr(c ^ ord(key[i % len(key)])) for i, c in enumerate(b64decode(string))
    )

def encode(string: str, key: str) -> str:
    if not key.isnumeric():
        raise InvalidXORKey('Invalid XOR key')
    return b64encode(bytes(
        ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(string)
    )).decode()