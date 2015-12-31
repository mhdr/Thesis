from datetime import datetime
import rsa

publicFile=open("public.pem")
publicData=publicFile.read()
publicFile.close()

privateFile=open("private.pem")
privateData=privateFile.read()
privateFile.close()

privateKey=rsa.PrivateKey.load_pkcs1(privateData)
publicKey=rsa.PublicKey.load_pkcs1(publicData)

f=open("test.txt")
message=f.read()
f.close()

print(datetime.now())

index=0

while index<1024 * 1024:
    m=message[index:index+240]
    index=index+240
    encrypted=rsa.encrypt(m,publicKey)
print(datetime.now())

#decryptedB=rsa.decrypt(encrypted,privateKey)