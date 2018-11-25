import socket
import sys
import Utils.utils as u
import Protocol.protocol as proto

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

query = proto.Ultra(O=proto.CONNECTING, f=(proto.PUSH, proto.SYN), n=100)
print(query)
sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
data = sock.recv(1024)
response = proto.Ultra.parse(str(data, "ascii"))
print(response)
ack = int(response.flags_id[0]) + 1
session_id = int(response.session_id)
query = proto.Ultra(O=proto.CONNECTING, I=session_id, f=(proto.ACK, proto.SYN), n=ack)
print("CONNECTED\n", query)
sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
data = sock.recv(1024)
response = proto.Ultra.parse(str(data, "ascii"))
print(response)

sys.exit()
