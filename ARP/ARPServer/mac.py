import fcntl, socket, struct
from scapy.all import *

class MAC:

    @staticmethod
    def get_local_mac(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])

    @staticmethod
    def get_remote_mac(ip):
        ans,unans = srp(ARP(pdst=ip), timeout=5, retry=3)
        for s,r in ans:
            return r[Ether].src