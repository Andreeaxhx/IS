from random import randint
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

START_MESSAGE="PUTEM INCEPE COMUNICAREA"
def string_to_binary(K):
    binary_K = ''
    for k in K:
        b=''.join(format(ord(i), 'b') for i in k)
        while len(b)<8:
            b="0"+b
        binary_K=binary_K+b
    if len(binary_K)!=128:
        print("string_to_binary %s returneaza o cheie de lungime diferita de 128!!!" % K)
    return binary_K

def XOR(binA, binB):
    i=0
    xor=''
    if(len(binA)!=128 or len(binB)!=128):
        print("Cheile nu au lungimea de 128!!!")
    if(len(binA)==len(binB)==128):
        while i<len(binA):
            if binA[i]!=binB[i]:
                xor=xor+'1'
            else:
                xor=xor+'0'
            i+=1
    return xor

def binary_to_character(binary):
    decimal, exp = 0, 0
    for i in range(len(binary)-1, -1, -1):
        dec=int(binary[i])
        decimal=decimal+dec*pow(2, exp)
        exp+=1
    return decimal

def binary_to_string(binary):
    string=''
    temp=''
    for i in range(0, len(binary), 8):
        temp=binary[i:i+8]
        string=string+chr(binary_to_character(temp))
    return string

def divide_into_16(plaintext):
    list_of_blocks=[]
    while len(plaintext)%16!=0:
        plaintext+=' '
    for i in range(0, len(plaintext), 16):
        list_of_blocks.append(plaintext[i:i+16])
    #print(list_of_blocks)
    return list_of_blocks

def generate_key(length):
    key=''
    for i in range(0, length):
        key=key+chr(randint(33, 126))

    return key

def generate_CBC_OFB():
    lst=["CBC", "OFB"]
    return lst[randint(0, 1)]

def encryption(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv, ciphered_data

def decryption(iv, data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    original_data = unpad(cipher.decrypt(data), AES.block_size)
    return original_data

def CBC_encryption(iv, key, plaintext):

    ciphertext_blocks=[]
    key_binary=string_to_binary(key)

    plaintext_blocks=divide_into_16(plaintext) #plaintextul impartit in blocuri de text a cate 16 caractere
    if plaintext_blocks[0]!=None:
        pass
        #print(plaintext_blocks[0])
    else:
        print("plaintext_blocks[0] este null")
    Y=XOR(string_to_binary(iv), string_to_binary(plaintext_blocks[0]))
    ciphertext_blocks.append(XOR(Y, key_binary))

    for i in range(1, len(plaintext_blocks)):
        Y=XOR(ciphertext_blocks[i-1], string_to_binary(plaintext_blocks[i]))
        ciphertext_blocks.append(XOR(Y, key_binary))

    return ciphertext_blocks #binar

def CBC_decryption(iv, key, ciphertext_blocks):

    plaintext_blocks=[]
    key_binary = string_to_binary(key)

    Y = XOR(key_binary, ciphertext_blocks[0])
    plaintext_blocks.append(XOR(Y, string_to_binary(iv)))

    for i in range(1, len(ciphertext_blocks)):
        Y = XOR(ciphertext_blocks[i], key_binary)
        plaintext_blocks.append(XOR(Y, ciphertext_blocks[i - 1]))

    return plaintext_blocks

def OFB_encryption(iv, key, plaintext):

    ciphertext_blocks=[]
    key_binary=string_to_binary(key)

    plaintext_blocks=divide_into_16(plaintext)

    Y=XOR(key_binary, string_to_binary(iv))
    ciphertext_blocks.append(XOR(string_to_binary(plaintext_blocks[0]), Y))

    for i in range(1, len(plaintext_blocks)):
        Y=XOR(key_binary, Y)
        ciphertext_blocks.append(XOR(string_to_binary(plaintext_blocks[i]), Y))

    return ciphertext_blocks #binar

def OFB_decryption(iv, key, ciphertext_blocks):

    plaintext_blocks=[]
    key_binary = string_to_binary(key)

    Y = XOR(key_binary, string_to_binary(iv))
    plaintext_blocks.append(XOR(Y, ciphertext_blocks[0]))

    for i in range(1, len(ciphertext_blocks)):
        Y = XOR(key_binary, Y)
        plaintext_blocks.append(XOR(Y, ciphertext_blocks[i]))

    return plaintext_blocks
