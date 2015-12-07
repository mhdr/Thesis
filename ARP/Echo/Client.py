import socket
from datetime import datetime
import time
import pickle

params={}

while True:
    HOST = '127.0.0.1'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    params["name"]="Mahmood"
    params["time"]=datetime.now()
    data=pickle.dumps(params)

    s.sendall(data)

    data_recv = s.recv(1024)
    data = bytearray()

    s.settimeout(1)

    while len(data_recv) > 0:
        data.extend(data_recv)

        if len(data_recv) < 1024:
            break

        try:
            data_recv = s.recv(1024)
        except socket.timeout:
            break

    paramsRcvd = pickle.loads(data)
    print(paramsRcvd)

    s.close()
    time.sleep(1)