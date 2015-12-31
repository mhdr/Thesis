

f=open("test.txt",mode="wb")

size=1024 * 1024

f.write("\0" * size)
f.close()