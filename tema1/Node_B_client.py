from functii import string_to_binary, XOR, binary_to_string, decryption, START_MESSAGE, CBC_decryption, OFB_decryption
import socket

K_prim = "fUjXn2r5u8x/A?D("
iv_CBC_OFB = "D*G-KaPdSgVkYp3s"

clientsocket=socket.socket()

port = 1233
host = "localhost"

print("wait for connection")
try:
    clientsocket.connect((host, port))
except socket.error as e:
    print(str(e))

clientsocket.send("B".encode('utf-8'))

from_server=clientsocket.recv(1024)
print(from_server.decode("utf-8"))

from_server=clientsocket.recv(1024)
#mod_operare=''
mod_operare=from_server.decode("latin-1")
if mod_operare!="OCB" or mod_operare!="OFB":
    mod_operare = from_server.decode("utf-8")

print("Modul de operare este: ", mod_operare)
from_server=clientsocket.recv(1024)
key_K=from_server

from_server=clientsocket.recv(1024)
i_v=from_server

key_K_decr=decryption(i_v, key_K, bytes(K_prim, 'utf-8'))
print("K decrypted: ", key_K_decr.decode('latin-1'))

clientsocket.send(START_MESSAGE.encode('utf-8'))

from_server=clientsocket.recv(2048)
lungime_lista=int(from_server.decode('utf-8'))

lista_blocuri=[]
for i in range(0, lungime_lista):
    lista_blocuri.append(clientsocket.recv(128).decode('utf-8'))

#print("lista blocuri: ", lista_blocuri)
plaintext_blocks=[]
if mod_operare=="CBC":
    plaintext_blocks = CBC_decryption(iv_CBC_OFB, key_K_decr.decode('utf-8'), lista_blocuri) #binary
elif mod_operare=="OFB":
    plaintext_blocks = OFB_decryption(iv_CBC_OFB, key_K_decr.decode('utf-8'), lista_blocuri)  # binary

print("Decrypted text with: ", mod_operare)
for i in plaintext_blocks:
    print(binary_to_string(i), end="")


clientsocket.close()