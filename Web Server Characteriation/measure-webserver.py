from scapy.all import *
import sys

from scapy.layers.inet import TCP, IP
from scapy.plist import _PacketList, _Inner

host = sys.argv[2]
port = int(sys.argv[3])


def printAverage(averageLatency: float) -> None:
    print("AVERAGELATENCY: " + averageLatency.__str__())


def readProcessFile(pcap_filename: str) -> Dict[str, _PacketList[_Inner]]:
    try:
        processed_file = rdpcap(pcap_filename)
    except Exception as e:
        print(f"ERROR: Could not read file {e}")
        sys.exit(1)
    return processed_file.sessions()


def validatePacket(packetX: _Inner) -> bool:
    if packetX.haslayer(TCP) and packetX.haslayer(IP):
        print("Validating packet IP: " + packetX[IP].src)
        print("Validating packet TCP: ", int(packetX[TCP].sport))
        return packetX[IP].src == host and int(packetX[TCP].sport) == port
    return False


def main():
    load_layer("http")
    sessions = readProcessFile(sys.argv[1])
    sessionsC = 0
    counter = 0
    for session in sessions:
        sessionsC += 1
        print("SESSION: " + str(sessionsC))
        for packetX in sessions[session]:
            if validatePacket(packetX):
                print("Showing packet: ")
                print(packetX.show())
                counter += 1
                print("PACKET: " + str(counter))
                print(packetX.summary())
                print(packetX.fields)
                print("Sent Time: ", packetX.sent_time)
                print("Time: ", packetX.time)
                exit(1)


if __name__ == "__main__":
    main()
