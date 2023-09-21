#!/usr/bin/env python

"""
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student

DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
"""

from socket import socket, AF_INET, SOCK_DGRAM
import struct, socket
from datetime import datetime


def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    host = server
    port = port
    buf = 1024
    address = (host, port)
    msg = b'\x1b' + 47 * b'\0'

    T1 = datetime.utcnow()
    soc = socket.socket(AF_INET, SOCK_DGRAM)
    soc.sendto(msg, address)
    msg, address = soc.recvfrom(buf)

    # t = struct.unpack('!12I', msg)[10]
    struct.unpack('!12I', msg[:48])
    T4 = datetime.utcnow()
    return msg, T1.timestamp(), T4.timestamp()


def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    unpacked = struct.unpack('!12I', pkt[:48])
    T2 = datetime.utcfromtimestamp((unpacked[9] / 1000000000) - 2208988800 + unpacked[8])
    T3 = datetime.utcfromtimestamp((unpacked[11] / 1000000000) - 2208988800 + unpacked[10])
    rtt = (T4 - T1) - (T3.timestamp() - T2.timestamp())
    offset = ((T2.timestamp() - T1) + (T3.timestamp() - T4)) / 2
    return rtt, offset


def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
    offsets = []
    for i in range(iters):
        (pkt, T12, T42) = getNTPTimeValue(server, port)
        (RTT, offset) = ntpPktToRTTandOffset(pkt, T12, T42)
        offsets.append(offset)

    currentTime = (sum(offsets) / len(offsets)) + datetime.now().timestamp()
    return datetime.utcfromtimestamp(currentTime).timestamp()


if __name__ == "__main__":
    print(getCurrentTime())
