import sys
import socket

if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    messageFileName = sys.argv[3]
    signatureFileName = sys.argv[4]

    messageFile = open(messageFileName)
    Lines = messageFile.readlines()

    for line in Lines:
        bytesT = bytes(line, 'utf-8')
