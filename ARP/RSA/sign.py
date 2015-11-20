import rsa

(publicKey,privateKey)=rsa.newkeys(2048,poolsize=4)

message="Hello World"
signature=rsa.sign(message,privateKey,"SHA-256")

result=rsa.verify(message,signature,publicKey)
print(result)

message2="Hello World 2"
try:
    rsa.verify(message2,signature,publicKey)
except rsa.VerificationError:
    print(False)