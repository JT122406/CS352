from scapy.all import *
import sys


def printAverage(averageLatency: float):
    print("AVERAGELATENCY: " + averageLatency.__str__())


def main():
    processed_file = rdpcap(sys.argv[1])
    sessions = processed_file.sessions()
    for packet in sessions:
        numPacket = numPacket + 1
    host = sys.argv[2]
    port = int(sys.argv[3])


if __name__ == "__main__":
    main()
