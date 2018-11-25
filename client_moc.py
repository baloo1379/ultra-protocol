import socket
import sys
import Utils.utils as u
import Protocol.protocol as proto

HOST, PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = proto.Ultra(O=proto.CONNECTING, f=(proto.PUSH, proto.SYN), n=100)
u.debugger(data)
sock.sendto(bytes(str(data), "ascii"), (HOST, PORT))

sys.exit()
