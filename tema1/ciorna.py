from random import randint

from Cryptodome.Random import get_random_bytes

aux=b'\xf0\xc8\x92\xea\x93\xb8P\x19\x9a\xa9\x1a\xf8\xc1\x8c\xd8W\xee\xb0\xbdD\xc1q]\x13\x1b\xbcph\x15Y\xdeb'

aux2=aux.hex()
print(aux2)
print(bytes.fromhex(aux2).decode('latin-1'))

from functii import generate_key

key = get_random_bytes(16)
print(type(key))
print(bytes.fromhex(key.hex()).decode('latin-1'))