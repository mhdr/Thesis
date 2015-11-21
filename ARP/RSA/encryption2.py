import rsa

publicFile=open("public.pem")
publicData=publicFile.read()
publicFile.close()

privateFile=open("private.pem")
privateData=privateFile.read()
privateFile.close()

privateKey=rsa.PrivateKey.load_pkcs1(privateData)
publicKey=rsa.PublicKey.load_pkcs1(publicData)

message="Hello World"

messageB=message.encode("UTF-8")

encrypted=rsa.encrypt(messageB,publicKey)

decryptedB=rsa.decrypt(encrypted,privateKey)
decrypted=decryptedB.decode("UTF-8")
print decrypted