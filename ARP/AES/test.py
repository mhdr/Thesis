from AESCipher import AESCipher

a=AESCipher("0123456789ABCDEF")
b=AESCipher("0123456789ABCDEF")

message= a.encrypt("Hello World")
print(message)

decryped=b.decrypt(message)
print(decryped)