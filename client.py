import socket
import sys
import random
import Protocol.protocol as proto
HOST, PORT = "localhost", 9999
data = input("message to send")



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = proto.Ultra(O=proto.CONNECTING, f=(proto.PUSH, proto.SYN), n = random.randrange(0,2000))
ack_n = int(packet.flags_id[0]) + 1
str(packet)
sock.sendto(bytes(packet + "\n", "ascii"), (HOST, PORT))



rec = proto.Ultra()
received = str(sock.recv(1024), "ascii")
rec = rec.parse(received)
resend = proto.Ultra(O=proto.CONNECTING, f=(proto.ACK, proto.SYN), n=ack_n)
if rec.proto.ACK == ack_n:
    sock.sendto(bytes(resend + "\n", "ascii"), (HOST, PORT))
else:
    print("received ack is different than expected cannot connect")



print("Sent:     {}".format(data))
print("Received: {}".format(received))
sys.exit()
