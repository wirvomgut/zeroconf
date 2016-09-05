#!/usr/bin/env python
# coding: utf8

""" Example of announcing a service (in this case, a fake HTTP server) """

import logging
import socket
import sys
import signal
import atexit
import os

from time import sleep

from zeroconf import ServiceInfo, Zeroconf

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def signal_handler(signal, frame):
    sys.exit(0)


def on_known():
    pass


def on_unknown():
    pass


def on_shutdown():
    print("Unregistering...")
    zeroconf.unregister_service(info)
    zeroconf.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    write_pid()
    
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(on_shutdown)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       "Kleine Reithalle Aussen._http._tcp.local.",
                       socket.inet_aton(get_ip()), 80, 0, 0,
                       desc, socket.gethostname())

    zeroconf = Zeroconf()
    print("Registration of a service")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
