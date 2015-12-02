import rsa
import uuid
from scapy.all import *
import threading
from datetime import datetime
from datetime import timedelta
import copy
from colorama import Fore

from ARPPacket import ARPPacket
from IPMAC import IPMAC
import socket
from Message import Message


ip_mac_list=[]
hacker_mac_list=[]
counter=0

def get_counter():
    lock=threading.BoundedSemaphore()

    global counter

    lock.acquire()

    counter=counter+1

    lock.release()

    return counter


def check_packet(pkt):
    if ARP in pkt:
        arp= pkt[ARP]

        if isinstance(arp,ARP):

            op=arp.fields["op"]
            # replay
            if op==2:
                arpPacket=ARPPacket(arp.fields["hwtype"],arp.fields["ptype"],arp.fields["hwlen"],
                                    arp.fields["plen"],arp.fields["op"],arp.fields["hwsrc"],
                                    arp.fields["psrc"],arp.fields["hwdst"],arp.fields["pdst"])
                ip_mac_list.append(arpPacket)
                print("{0} - ".format(get_counter()) +  Fore.GREEN + "psrc : {0} , hwsrc : {1} ==> ARP Packet + : {2}".format(arpPacket.SenderProtocolAddress,
                                                                               arpPacket.SenderHardwareAddress,
                                                                               len(ip_mac_list)) + Fore.RESET)


def sniffPackets():
    sniff(prn=lambda x : check_packet(x), filter="arp")

def garbage_collector():
    while True :
        if len(ip_mac_list)>0:
            for arp in ip_mac_list:
                if isinstance(arp,ARPPacket):
                    now=datetime.now()
                    delta=timedelta(seconds=60)
                    if now-arp.Time>delta:
                        ip_mac_list.remove(arp)
                        print("{0} - ".format(get_counter()) +
                              Fore.YELLOW + "psrc : {0} , hwsrc : {1} ==> ARP Packet - : {2}".format(arp.SenderProtocolAddress,
                                                                               arp.SenderHardwareAddress,
                                                                                       len(ip_mac_list)) + Fore.RESET)

        time.sleep(0.1)

def filter_by_ip(lst,ip):
    """
    filter by ip
    :param lst: a list of ARPPackets
    :param ip: filter
    :return: a list of ARPPackets that is filtered by ip
    :type lst:list
    :type ip:str
    :rtype:list
    """

    result=[]

    for ipmac in lst:
        if isinstance(ipmac,IPMAC):
            if ipmac.IP==ip:
                result.append(ipmac)

    return result

def filter_by_mac(lst,mac):
    """
    filter by mac
    :param lst: a list of ARPPackets
    :param ip: filter
    :return: a list of ARPPackets that is filtered by mac
    :type lst:list
    :type ip:str
    :rtype:list
    """

    result=[]

    for ipmac in lst:
        if isinstance(ipmac,IPMAC):
            if ipmac.MAC==mac:
                result.append(ipmac)

    return result

def contains(lst,ip,mac):
    """

    :param lst:
    :param ip:
    :param mac:
    :return:
    :type lst:list
    :type ip:str
    :type mac:str
    :rtype:list
    """

    if len(lst)==0:
        return False

    for ipmac in lst:
        if isinstance(ipmac,IPMAC):
            if ipmac.IP==ip and ipmac.MAC==mac:
                return True

    return False

def detect_attack():

    while True:
        #new_ip_mac_list=copy.copy(ip_mac_list) just copy the list by value, not the members
        new_ip_mac_list=copy.deepcopy(ip_mac_list) # copy list and its member by value

        if len(new_ip_mac_list)==0:
            continue

        unique_pairs=[]

        for arp in new_ip_mac_list:
            if isinstance(arp,ARPPacket):
                if contains(unique_pairs,arp.SenderProtocolAddress,arp.SenderHardwareAddress):
                    pass
                else:
                    ipmac=IPMAC(arp.SenderProtocolAddress,arp.SenderHardwareAddress)
                    unique_pairs.append(ipmac)

        for ipmac2 in unique_pairs:
            if isinstance(ipmac2,IPMAC):
                filtered_ipmac=filter_by_mac(unique_pairs,ipmac2.MAC)
                count=len(filtered_ipmac)

                if count>1:
                    if ipmac2.MAC in hacker_mac_list:
                        pass
                    else:
                        hacker_mac_list.append(ipmac2.MAC)
                        print("{0} - ".format(get_counter()) + Fore.RED + "{0} is attacking".format(ipmac2.MAC) + Fore.RESET)
                else:
                    if ipmac2.MAC in hacker_mac_list:
                        hacker_mac_list.remove(ipmac2.MAC)
                        print("{0} - ".format(get_counter()) + Fore.MAGENTA + "{0} is no longer attacking".format(ipmac2.MAC) + Fore.RESET)

        time.sleep(0.1)

def get_message1():
    macs=copy.deepcopy(hacker_mac_list)

    privateFile=open("private.pem")
    privateData=privateFile.read()
    privateFile.close()

    privateKey=rsa.PrivateKey.load_pkcs1(privateData)

    uid=str(uuid.uuid1())
    m=Message.get_sum(macs,uid)

    signature=rsa.sign(m,privateKey,"SHA-256")

    message=Message(macs,uid,signature)
    return message.dumps()


def run_server():
    HOST = ''
    PORT = 11000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)

    while True:
        conn, addr = s.accept()
        print("{0} - ".format(get_counter()) + 'Connection from : {0}'.format(addr))

        data_recv=conn.recv(1024)
        data=bytearray()

        conn.settimeout(1)

        while len(data_recv)>0:
            data.extend(data_recv)
            try:
                data_recv=conn.recv(1024)
            except socket.timeout:
                break

        data=str(data)
        if data=="1":
            message=get_message1()
            conn.sendall(message)
        conn.close()

threading.Thread(target=sniffPackets).start()
threading.Thread(target=garbage_collector).start()
threading.Thread(target=detect_attack).start()
threading.Thread(target=run_server).start()