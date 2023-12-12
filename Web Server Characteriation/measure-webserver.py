from scapy.all import *
import sys

from scapy.layers.inet import TCP, IP
from scapy.plist import _PacketList, _Inner

destHost = sys.argv[2]
destPort = int(sys.argv[3])


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
    return packetX.haslayer(TCP).__bool__() and packetX.haslayer(IP).__bool__()


def main():
    load_layer("http")
    sessions = readProcessFile(sys.argv[1])
    counter = 0
    responses = []
    requests = []
    for session in sessions:
        for packetX in sessions[session]:
            if validatePacket(packetX):
                if packetX[IP].dst == destHost and packetX[TCP].dport == destPort:
                    requests.append(packetX)
                elif packetX[IP].src == destHost and packetX[TCP].sport == destPort:
                    responses.append(packetX)


                print("Showing packet: ")
                print(packetX.show())
                counter += 1
                print("PACKET: " + str(counter))
                print(packetX.summary())
                print(packetX.fields)
                print("Sent Time: ", packetX.sent_time)
                print("Time: ", packetX.time)


if __name__ == "__main__":
    main()
