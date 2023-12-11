from scapy.all import *
import sys


def printAverage(averageLatency: float):
    print("AVERAGELATENCY: " + averageLatency.__str__())


def readProcessFile(pcap_filename: str):
    processed_file = rdpcap(pcap_filename)
    return processed_file.sessions()


def main():
    load_layer("http")
    sessions = readProcessFile(sys.argv[1])
    host = sys.argv[2]
    port = int(sys.argv[3])
    counter = 0
    for session in sessions:
        for packetX in sessions[session]:
            counter += 1


if __name__ == "__main__":
    main()
