import socket
import threading
from colorama import Fore
from datetime import datetime
from datetime import timedelta
import os

import time

from Message import Message

counter=0
mac_list=[]

timer_initial_value=5
timer=timer_initial_value
is_traffic_blocked=False

def get_counter():
    lock=threading.BoundedSemaphore()

    global counter

    lock.acquire()

    counter=counter+1

    lock.release()

    return counter

def fetch():

    while True:
        global HOST
        global PORT
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
            if False:assert isinstance(message,Message)

            current_time=datetime.now()

            if len(message.macs)>0:
                if message.verify():

                    if current_time - message.time < timedelta(seconds=5):

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

                        reset_timer()
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

                reset_timer()

        time.sleep(1)

def get_arp_server_mac():
    while True:
        global HOST
        global PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(b'2')

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

        mac=data

        return mac


def block_traffic():
    global is_traffic_blocked
    global arp_server_mac

    cmd1="arptables -P INPUT DROP"
    cmd2="arptables -A INPUT --source-mac {0} -j ACCEPT".format(arp_server_mac)

    os.system(cmd1)
    os.system(cmd2)

    is_traffic_blocked=True


def allow_traffic():
    global is_traffic_blocked

    os.system("arptables -P INPUT ACCEPT")
    os.system("arptables -F")
    os.system("ip neighbour flush all")

    is_traffic_blocked=False

def run_timer():

    global timer
    global is_traffic_blocked

    while True:

        time.sleep(1)

        if timer>0:

            timer=timer-1
        else:
            if is_traffic_blocked==False:
                block_traffic()

def reset_timer():
    lock=threading.BoundedSemaphore()

    global timer
    global timer_initial_value
    global is_traffic_blocked

    lock.acquire()

    timer=timer_initial_value

    if is_traffic_blocked==True:
        allow_traffic()

    lock.release()


HOST = '192.168.1.104'
PORT = 11000

os.system("arptables -F")
os.system("iptables -F")
arp_server_mac=get_arp_server_mac()
threading.Thread(target=fetch).start()
threading.Thread(target=run_timer).start()