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
signature=rsa.sign(message,privateKey,"SHA-256")

result=rsa.verify(message,signature,publicKey)
print(result)

message2="Hello World 2"
try:
    rsa.verify(message2,signature,publicKey)
except rsa.VerificationError:
    print(False)