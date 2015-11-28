
def enable():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
            ipf.write('1\n')

def disable():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('0\n')

disable()