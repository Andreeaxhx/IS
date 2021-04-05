from Cryptodome.Random import get_random_bytes
from functii import string_to_binary, XOR, generate_key, encryption
import socket

K=get_random_bytes(16)
#K = generate_key(16)
#K = "eThWmZq4t7w!z%C*"
K_prim = "fUjXn2r5u8x/A?D("

clientsocket=socket.socket()

port = 1233
host = "localhost"

print("wait for connection")
try:
    clientsocket.connect((host, port))
except socket.error as e:
    print(str(e))

clientsocket.send("KM".encode('utf-8'))

from_server=clientsocket.recv(1024)
print(from_server.decode("utf-8"))

from_server=clientsocket.recv(1024)
print(from_server.decode("utf-8"))

if from_server.decode("utf-8")=="[node A] hei, Key Manager, give me the K key":
    iv, new_K=encryption(bytes(bytes.fromhex(K.hex()).decode('latin-1'), 'utf-8'), bytes(K_prim, 'utf-8'))
    #iv, new_K=encryption(bytes(K, 'utf-8'), bytes(K_prim, 'utf-8'))
    clientsocket.send(iv)
    clientsocket.send(new_K)

print(bytes.fromhex(K.hex()).decode('latin-1'))
#print(K)

clientsocket.close()