from functii import generate_CBC_OFB, string_to_binary, XOR, binary_to_string, decryption, START_MESSAGE, CBC_encryption, OFB_encryption
import socket
from _thread import *

K_prim = "fUjXn2r5u8x/A?D("
iv_CBC_OFB = "D*G-KaPdSgVkYp3s"
mod_operare = generate_CBC_OFB()
#mod_operare = "OCB"

global key_encr, iv, key_decr
key=''; iv=''; key_decr=''

serversocket = socket.socket()

host="localhost"
port=1233
no_of_threads=0

try:
    serversocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("waiting for connection")
serversocket.listen(5)

def client_thread(connection, node):
    from_client = connection.recv(1024)
    which_node = from_client.decode('utf-8')
    if which_node=="KM":
        message="[node A] welcome to the server, node KM"
    elif which_node=="B":
        message = "[node A] welcome to the server, node B"
    connection.send(str.encode(message))

    while True:
        if node==0:
            message="[node A] hei, Key Manager, give me the K key"
        elif node==1:
            message=str(mod_operare)

        connection.send(message.encode('utf-8'))

        if node==0:
            message_recv = connection.recv(2048)
            i_v=message_recv

            message_recv = connection.recv(2048)
            key_K = message_recv

            listOfGlobals = globals()
            listOfGlobals["key_encr"] = key_K
            listOfGlobals["iv"] = i_v

            key_K_decr=decryption(i_v, key_K, bytes(K_prim, 'utf-8'))
            print("K decrypted: ", key_K_decr.decode('utf-8'))
            listOfGlobals["key_decr"] = key_K_decr.decode('utf-8')
            break

        if node==1:
            connection.send(key_encr)
            connection.send(iv)
            from_client=connection.recv(1024)

            if from_client.decode('utf-8')==START_MESSAGE:
                print("am primit de la B: ", from_client.decode("utf-8"))

            input=open("file.txt", "r").read()


            if mod_operare=="CBC":
                encrypted_input=CBC_encryption(iv_CBC_OFB, key_decr, input)
            elif mod_operare=="OFB":
                encrypted_input=OFB_encryption(iv_CBC_OFB, key_decr, input)


            #print(encrypted_input)

            lungime_lista=len(encrypted_input)
            connection.send(str(lungime_lista).encode('utf-8'))
            #print(lungime_lista)

            for i in range(0, lungime_lista):
                connection.send(encrypted_input[i].encode('utf-8'))
                print(binary_to_string(encrypted_input[i]))

            break
        #connection.sendall(str.encode(reply))

    connection.close()

currentNode=0
while True:
    client, address = serversocket.accept()
    print("connected to: "+str(address[0])+"--"+str(address[1]))
    start_new_thread(client_thread, (client, currentNode))
    currentNode+=1
    no_of_threads+=1
    print("Number of threads", no_of_threads)


serversocket.close()