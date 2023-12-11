from scapy.all import *
import sys

from scapy.layers.inet import TCP, IP
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
            if packetX.haslayer(TCP) and packetX.haslayer(IP):
                ip_src = packetX["IP"].src
                ip_dst = packetX["IP"].dst
                tcp_sport = packetX["TCP"].sport
                tcp_dport = packetX["TCP"].dport

                if ip_dst == host and tcp_dport == port:
                    # HTTP response
                    responses[(ip_src, tcp_sport)].append(packet.time)
                elif ip_src == host and tcp_sport == port:
                    # HTTP request
                    requests[(ip_dst, tcp_dport)].append(packet.time)

                counter += 1
                print("PACKET: " + str(counter))
                print(packetX.summary())
                print(packetX.fields)
                print("Sent Time: ", packetX.sent_time)
                print("Time: ",packetX.time)


if __name__ == "__main__":
    main()
