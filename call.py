import os
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from time import sleep

PORT = 50000
MAGIC = "fna349fn"

def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def write_pid():
    pid = os.getpid()
    op = open("./wvg-zeroconf.pid","w")
    op.write("%s" % pid)
    op.close()

write_pid()

s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket

while 1:
    data = MAGIC+get_ip()
    s.sendto(data, ('<broadcast>', PORT))
    print("sent service announcement")
    sleep(5)
