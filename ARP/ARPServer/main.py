from scapy.all import *

from ARPPacket import ARPPacket

ip_mac_list=[]

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
                print(len(ip_mac_list))


sniff(prn=lambda x : check_packet(x), filter="arp")