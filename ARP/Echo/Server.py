import socket
import pickle

from datetime import datetime

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

while True:
    conn, addr = s.accept()

    data_recv = conn.recv(1024)
    data = bytearray()

    conn.settimeout(1)

    while len(data_recv) > 0:
        data.extend(data_recv)

        if len(data_recv)<1024 :
            break

        try:
            data_recv = conn.recv(1024)
        except socket.timeout:
            break

    paramsRcvd=pickle.loads(data)
    print(paramsRcvd)

    params={}

    params["name"]=paramsRcvd["name"]
    params["time"]=datetime.now()

    message = pickle.dumps(params)
    conn.sendall(message)
    conn.close()
