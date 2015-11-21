import rsa

(publicKey,privateKey)=rsa.newkeys(2048,poolsize=4)
publicData=publicKey.save_pkcs1()
privateData=privateKey.save_pkcs1()

publicFile=open("public.pem",mode="w+")
publicFile.write(publicData)
publicFile.close()

privateFile=open("private.pem",mode="w+")
privateFile.write(privateData)
privateFile.close()