from binascii import hexlify
from DiffieHellman import DiffieHellman

a = DiffieHellman()
b = DiffieHellman()

a.genKey(b.publicKey)
b.genKey(a.publicKey)

#a.showParams()
#a.showResults()
#b.showParams()
#b.showResults()

if(a.getKey() == b.getKey()):
    print("Shared keys match.")
    print("Key:", hexlify(a.key))
else:
    print("Shared secrets didn't match!")
    print("Shared secret A: ", a.genSecret(b.publicKey))
    print("Shared secret B: ", b.genSecret(a.publicKey))