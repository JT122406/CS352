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
    return msg, T1.timestamp(), T4.timestamp()

def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    unpacked = struct.unpack('!12I', pkt[:48])
    T2 = datetime.utcfromtimestamp((unpacked[9]/1000000000) - 2208988800 + unpacked[8])
    T3 = datetime.utcfromtimestamp((unpacked[11]/1000000000) - 2208988800 + unpacked[10])
    rtt = (T4 - T1) - (T3.timestamp() - T2.timestamp())
    offset = ((T2.timestamp() - T1) + (T3.timestamp() - T4)) / 2 
    return rtt, offset


def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
    offsets = []
    for i in range(iters):
        (pkt, T12, T42) = getNTPTimeValue(server, port)
        (RTT, offset) = ntpPktToRTTandOffset(pkt, T12, T42)
        offsets.append(offset)

    currentTime = (sum(offsets)/len(offsets)) + datetime.utcnow().timestamp()
    return datetime.utcfromtimestamp(currentTime).timestamp()


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
    print(datetime.fromtimestamp((unpacked[9]/1000000000) + unpacked[8] - 2208988800))
    #print(datetime.utcfromtimestamp(unpacked[10] - 2208988800))
    print(datetime.fromtimestamp((unpacked[11]/1000000000) - 2208988800 +unpacked[10]))
    T1 = B
    T4 = C
    T2 = datetime.utcfromtimestamp((unpacked[9]/1000000000) - 2208988800 +unpacked[8]) 
    T3 = datetime.utcfromtimestamp((unpacked[11]/1000000000) - 2208988800 +unpacked[10])  
    print("this is in order now")
    print(datetime.fromtimestamp(T1))
    print(T2)
    print(T3)
    print(datetime.fromtimestamp(T4))
    #print(T4.timestamp())
    #print(T4.timestamp() - 100.5)
    #print("difference between T1 and T2", datetime.fromtimestamp(B - ((unpacked[9]/1000000000) - 2208988800 +unpacked[8])))
    #print("difference between T1 and T2", T2 - datetime.fromtimestamp(T1))
    #print("difference between T1 and T2", T2.timestamp() - T1)
    (Y,Z) = ntpPktToRTTandOffset(A, B, C)
    print("RTT", Y)
    print("Offset", Z)
    print("RTT", (datetime.utcfromtimestamp((T4 - T1)) - (T3 - T2)))
    print("Offset", ((T2 - datetime.utcfromtimestamp(T1)) + (T3 - datetime.utcfromtimestamp(T4))))
    print(datetime.fromtimestamp(getCurrentTime()))
    print(datetime.now())
    print(getCurrentTime())