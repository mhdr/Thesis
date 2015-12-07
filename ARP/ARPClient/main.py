import socket
import threading
from colorama import Fore
from datetime import datetime

import time

from Message import Message

counter=0

def get_counter():
    lock=threading.BoundedSemaphore()

    global counter

    lock.acquire()

    counter=counter+1

    lock.release()

    return counter

def fetch():

    while True:
        HOST = '192.168.1.104'
        PORT = 11000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(b'1')

        data_recv=s.recv(1024)
        data=bytearray()

        s.settimeout(1)

        while len(data_recv)>0:
            data.extend(data_recv)

            if len(data_recv) < 1024:
                break

            try:
                data_recv=s.recv(1024)
            except socket.timeout:
                break

        s.close()

        if len(data)>0:
            message= Message.loads(data)

            if len(message.macs)>0:
                if message.verify():
                    for mac in message.macs:
                        print("{0} - ".format(get_counter()) +  Fore.MAGENTA + "MAC : {0}".format(mac) + Fore.RESET)
                else:
                    print("{0} - ".format(get_counter()) +  Fore.RED + "We received some data,but it seems they are manipulated." + Fore.RESET)

            else:
                print("{0} - ".format(get_counter()) +  Fore.GREEN + "Safe" + Fore.RESET)

        time.sleep(1)


threading.Thread(target=fetch).start()