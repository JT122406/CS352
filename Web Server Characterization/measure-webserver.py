from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.inet import TCP, IP
from scapy.plist import _Inner

destHost = sys.argv[2]
destPort = int(sys.argv[3])
request_info = {}
response_times = []


def printAverage(averageLatency: float) -> None:
    print("AVERAGE LATENCY: " + round(averageLatency, 5).__str__())


def printPercentiles() -> None:
    sorted_times = sorted(response_times)
    length = len(sorted_times)

    percentile_25 = sorted_times[int(length * 0.25)]
    percentile_50 = sorted_times[int(length * 0.50)]
    percentile_75 = sorted_times[int(length * 0.75)]
    percentile_95 = sorted_times[int(length * 0.95)]
    percentile_99 = sorted_times[int(length * 0.99)]

    print(f"PERCENTILES: {percentile_25:.5f}, {percentile_50:.5f}, {percentile_75:.5f}, {percentile_95:.5f}, {percentile_99:.5f}")


def readProcessFile(pcap_filename: str) -> PacketList:
    try:
        processed_file = rdpcap(pcap_filename)
    except Exception as e:
        print(f"ERROR: Could not read file {e}")
        sys.exit(1)
    return processed_file


def validatePacket(packetX: _Inner) -> bool:
    return packetX.haslayer(TCP).__bool__() and packetX.haslayer(IP).__bool__()


def packetProcessor(packetX: _Inner) -> None:
    if validatePacket(packetX):
        source_ip = packetX[IP].src
        dst_ip = packetX[IP].dst
        source_port = packetX[TCP].sport
        dst_port = packetX[TCP].dport

        if packetX.haslayer(HTTPRequest) and dst_port == destPort and dst_ip == destHost:
            requestKey = (source_ip, dst_ip, source_port, dst_port)
            request_info[requestKey] = {'requestTime': packetX.time, 'responseTime': None}
        elif packetX.haslayer(HTTPResponse) and source_port == destPort and source_ip == destHost:
            responseKey = (dst_ip, source_ip, dst_port, source_port)

            if responseKey in request_info:
                requestTime = request_info[responseKey]['requestTime']

                response_times.append(packetX.time - requestTime)

                del request_info[responseKey]


def main():
    load_layer("http")
    packets = readProcessFile(sys.argv[1])
    for packet1 in packets:
        packetProcessor(packet1)

    averageLatency = sum(response_times) / len(response_times) if response_times else 0
    printAverage(averageLatency)
    printPercentiles()


if __name__ == "__main__":
    main()
