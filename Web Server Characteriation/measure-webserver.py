from scapy.all import *
import sys


def printAverage(averageLatency: float):
    print("AVERAGELATENCY: " + averageLatency.__str__())


def main():
    load_layer("http")
    processed_file = rdpcap(sys.argv[1])
    sessions = processed_file.sessions()
    counter = 0
    for session in sessions:
        for packetX in sessions[session]:
            counter += 1

    host = sys.argv[2]
    port = int(sys.argv[3])


if __name__ == "__main__":
    main()
