import socket
import sys
from protocol import *
from Utils import utils

HOST, PORT = "localhost", 9999
data = input("message to send")


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.sendto(bytes(data + "\n", "ascii"), (HOST, PORT))
received = str(sock.recv(1024), "ascii")

print("Sent:     {}".format(data))
print("Received: {}".format(received))
sys.exit()
