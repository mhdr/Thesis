from scapy.all import *
import threading
from datetime import datetime
from datetime import timedelta

from ARPPacket import ARPPacket

ip_mac_list=[]

# ip as key and mac as value
ip_mac_pairs={}

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
                print("+ : {0}".format(len(ip_mac_list)))


def sniffPackets():
    sniff(prn=lambda x : check_packet(x), filter="arp")

def garbageCollector():
    while True :
        if len(ip_mac_list)>0:
            for arp in ip_mac_list:
                if isinstance(arp,ARPPacket):
                    now=datetime.now()
                    delta=timedelta(seconds=30)
                    if now-arp.Time>delta:
                        ip_mac_list.remove(arp)
                        print("- : {0}".format(len(ip_mac_list)))

        time.sleep(0.1)

threading.Thread(target=sniffPackets).start()
threading.Thread(target=garbageCollector).start()