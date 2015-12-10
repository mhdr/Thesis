import socket
import threading
from colorama import Fore
from datetime import datetime
import os

import time

from Message import Message

counter=0
mac_list=[]

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

                        global mac_list
                        if mac not in mac_list:
                            cmd1="arptables -A INPUT --source-mac {0} -j DROP".format(mac)
                            cmd2="iptables -A INPUT -m mac --mac-source {0} -j DROP".format(mac)
                            cmd3="ip neighbour flush all"
                            os.system(cmd1)
                            os.system(cmd2)
                            os.system(cmd3)

                            mac_list.append(mac)

                        print("{0} - ".format(get_counter()) +  Fore.MAGENTA + "MAC : {0}".format(mac) + Fore.RESET)
                else:
                    print("{0} - ".format(get_counter()) +  Fore.RED +
                          "We received some data,but it seems they are manipulated." + Fore.RESET)

            else:

                global mac_list
                if False : assert isinstance(mac_list,list)

                for mac in mac_list:
                    cmd1="arptables -D INPUT --source-mac {0} -j DROP".format(mac)
                    cmd2="iptables -D INPUT -m mac --mac-source {0} -j DROP".format(mac)
                    os.system(cmd1)
                    os.system(cmd2)
                    mac_list.remove(mac)


                print("{0} - ".format(get_counter()) +  Fore.GREEN + "Safe" + Fore.RESET)

        time.sleep(1)

os.system("arptables -F")
os.system("iptables -F")
threading.Thread(target=fetch).start()