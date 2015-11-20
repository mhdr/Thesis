import hashlib

message="Hello World"
salt="salt"

output= hashlib.sha256(message+salt).hexdigest()
print(output)

message="Hello World 2"
salt="salt2"

output= hashlib.sha256(message+salt).hexdigest()
print(output)