#!/usr/bin/env python

'''
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student

DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
'''

from socket import socket, AF_INET, SOCK_DGRAM
import struct, socket, time
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

    #t = struct.unpack('!12I', msg)[10]
    t = struct.unpack('!12I', msg[:48])
    T4 = datetime.utcnow()
    return msg, T1, T4

def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # add your code here 
    return (rtt, offset)


def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
    times = []
    for i in range(iters):
        (pkt, T12, T42) = getNTPTimeValue(server, port)
        ntpPktToRTTandOffset(pkt, T12, T42)
        (RTT, offset) = ntpPktToRTTandOffset(pkt, T1, T4)
        times.append(datetime.now() + offset + RTT)

    currentTime = sum(times)/len(times)
    return currentTime


if __name__ == "__main__":
    #print(getCurrentTime())
    #print(getNTPTimeValue())
    A, B, C = getNTPTimeValue("clock.nyc.he.net", 123)
    print(B)
    print(C)
    #print(A)
    unpacked = struct.unpack('!12I', A[:48])
    #print(unpacked[11] - unpacked[10])
    print(unpacked)
    print(datetime.utcfromtimestamp((unpacked[9]/1000000000) + unpacked[8] - 2208988800))
    #print(datetime.utcfromtimestamp(unpacked[10] - 2208988800))
    print(datetime.utcfromtimestamp((unpacked[11]/1000000000) - 2208988800 +unpacked[10]))
    T1 = B
    T4 = C
    T2 = datetime.utcfromtimestamp((unpacked[9]/1000000000) - 2208988800 +unpacked[8]) 
    T3 = datetime.utcfromtimestamp((unpacked[11]/1000000000) - 2208988800 +unpacked[10])  
    print("this is in order now")
    print(T1)
    print(T2)
    print(T3)
    print(T4)