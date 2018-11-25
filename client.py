import socket
import sys
import random
import Protocol.protocol as proto
HOST, PORT = "localhost", 9999
data = input("message to send")
basic = proto.Ultra()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = proto.Ultra(O=proto.CONNECTING, f=(proto.PUSH, proto.SYN), n = random.randrange(0,2000))
ack_n = int(packet.flags_id[0]) + 1
packet = str(packet)
sock.sendto(bytes(packet, "ascii"), (HOST, PORT))



rec = proto.Ultra()
received = sock.recv(1024)
received = str(received, "ascii")
rec.parse(received)
basic.session_id = rec.session_id

if rec.proto.ACK == ack_n:
    resend = proto.Ultra(O=proto.CONNECTING, f=(proto.ACK, proto.SYN), n=ack_n)
    resend = str(resend)
    sock.sendto(bytes(resend, "ascii"), (HOST, PORT))

#while
    range1 = proto.Ultra()
    range = sock.recv(1024)
    range = str(range, "ascii")
    range1 = range1.parse(range)

else:
    print("received ack is different than expected cannot connect")



print("Sent:     {}".format(data))
print("Received: {}".format(received))
sys.exit()
