from scapy.all import *
import sys

from scapy.plist import _PacketList, _Inner


def printAverage(averageLatency: float):
    print("AVERAGELATENCY: " + averageLatency.__str__())


def readProcessFile(pcap_filename: str) -> Dict[str, _PacketList[_Inner]]:
    try:
        processed_file = rdpcap(pcap_filename)
    except Exception as e:
        print(f"ERROR: Could not read file {e}")
        sys.exit(1)
    return processed_file.sessions()


def main():
    load_layer("http")
    sessions = readProcessFile(sys.argv[1])
    host = sys.argv[2]
    port = int(sys.argv[3])
    sessionsC = 0
    counter = 0
    for session in sessions:
        sessionsC += 1
        print("SESSION: " + str(sessionsC))
        for packetX in sessions[session]:
            if packetX.haslayer("TCP") and packetX.haslayer("IP"):
                counter += 1
                print("PACKET: " + str(counter))
                print(packetX.summary())
                print(packetX.fields)


if __name__ == "__main__":
    main()
