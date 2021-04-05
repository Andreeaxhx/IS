from functii import XOR, string_to_binary, binary_to_string, divide_into_16
iv="D*G-KaPdSgVkYp3s"
key="Yp3s6v9y/B?E(H+M"

plaintext="It was my second day on the job. I was sitting in my seemingly gilded cubicle, overlooking Manhattan, " \
          "and pinching my right arm to make sure it was real. I landed an internship at Conde Nast Traveler. " \
          "Every aspiring writer I have ever known secretly dreamt of an Anthony Bourdain lifestyle. " \
          "Travel the world and write about its most colorful pockets. When my phone rang, and it was Mom telling " \
          "me Dad had a heart attack. He did not make it. I felt as though the perfectly carpeted floors had dropped" \
          " out from under me. Now that I have come out the other side, I realize Dad left me with a hefty stack of " \
          "teachings. Here are three ideals I know he would have liked for me to embrace."

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

ciphertext_blocks=OFB_encryption(iv, key, plaintext)
print("\nEncrypted text: ")
for i in ciphertext_blocks:
    print(binary_to_string(i), end="")

plaintext_blocks=OFB_decryption(iv, key, ciphertext_blocks) #binary
print("\n\nDecrypted text: ")
for i in plaintext_blocks:
    print(binary_to_string(i), end="")
