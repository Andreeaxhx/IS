from functii import XOR, string_to_binary, binary_to_string, divide_into_16, generate_key
iv="123456789Andreea"
key="!mY{nLgMC^(~.m5+"

plaintext="It was my second day on the job. I was sitting in my seemingly gilded cubicle, overlooking Manhattan, " \
          "and pinching my right arm to make sure it was real. I landed an internship at Conde Nast Traveler. " \
          "Every aspiring writer I have ever known secretly dreamt of an Anthony Bourdain lifestyle. " \
          "Travel the world and write about its most colorful pockets. When my phone rang, and it was Mom telling " \
          "me Dad had a heart attack. He did not make it. I felt as though the perfectly carpeted floors had dropped" \
          " out from under me. Now that I have come out the other side, I realize Dad left me with a hefty stack of " \
          "teachings. Here are three ideals I know he would have liked for me to embrace."

def CBC_encryption(iv, key, plaintext):

    ciphertext_blocks=[]
    key_binary=string_to_binary(key)

    plaintext_blocks=divide_into_16(plaintext) #plaintextul impartit in blocuri de text a cate 16 caractere

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

ciphertext_blocks=CBC_encryption(iv, key, plaintext)
print("\nEncrypted text with CBC: ")
for i in ciphertext_blocks:
    print(binary_to_string(i), end="")

plaintext_blocks=CBC_decryption(iv, key, ciphertext_blocks) #binary
print("\n\nDecrypted text with CBC: ")
for i in plaintext_blocks:
    print(binary_to_string(i), end="")
