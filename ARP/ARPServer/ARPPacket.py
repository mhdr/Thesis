from datetime import datetime

class ARPPacket:

    def __init__(self,hwtype,ptype,hwlen,plen,op,hwsrc,psrc,hwdst,pdst):
        self.HardwareType=hwtype
        self.ProtocolType=ptype
        self.HardwareLength=hwlen
        self.ProtocolLength=plen
        self.Operation=op
        self.SenderHardwareAddress=hwsrc # *
        self.SenderProtocolAddress=psrc # *
        self.TargetHardwareAddress=hwdst
        self.TargetProtocolAddress=pdst
        self.Time=datetime.now()
