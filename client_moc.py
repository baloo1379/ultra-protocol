import socket
import sys
from Protocol.protocol import *

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# connecting by client
query = Ultra(O=CONNECTING, f=(PUSH, SYN), n=100)
print(query)
sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
data = sock.recv(1024)
response = Ultra.parse(str(data, "ascii"))
print(response)
ack = int(response.flags_id[0]) + 1
session_id = int(response.session_id)
query = Ultra(O=CONNECTING, I=session_id, f=(ACK, SYN), n=ack)
print("CONNECTED\n", query)
sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
data = sock.recv(1024)
response = Ultra.parse(str(data, "ascii"))
print(response)

sys.exit()
