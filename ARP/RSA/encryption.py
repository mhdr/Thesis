import rsa

(publicKey,privateKey)=rsa.newkeys(512,poolsize=4)

message="Hello World"

messageB=message.encode("UTF-8")

encrypted=rsa.encrypt(messageB,publicKey)

decryptedB=rsa.decrypt(encrypted,privateKey)
decrypted=decryptedB.decode("UTF-8")
print decrypted