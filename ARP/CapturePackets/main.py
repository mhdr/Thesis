from scapy.all import *

use_assert=False

def print_packet(pkt):
    if use_assert:
        assert isinstance(pkt,Packet)

    if ARP in pkt:
        arp= pkt[ARP]

        if use_assert:
            assert isinstance(arp,ARP)

        print "hwtype : {0}".format(arp.fields["hwtype"])
        print "ptype : {0}".format(arp.fields["ptype"])
        print "hwlen : {0}".format(arp.fields["hwlen"])
        print "plen : {0}".format(arp.fields["plen"])
        print "op : {0}".format(arp.fields["op"])
        print "hwsrc : {0}".format(arp.fields["hwsrc"])
        print "psrc : {0}".format(arp.fields["psrc"])
        print "hwdst : {0}".format(arp.fields["hwdst"])
        print "pdst : {0}".format(arp.fields["pdst"])
        print("-----------------")


sniff(prn=lambda x : print_packet(x),filter="arp")

