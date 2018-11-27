import socket
import sys
from random import randrange
from Protocol.protocol import *


def client_moc(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # connecting by client
    # send
    query = Ultra(O=CONNECTING, f=(PUSH, SYN), n=100)
    print("S", query.print())
    sock.sendto(bytes(str(query), "ascii"), (host, port))

    # ack and session from server
    # recv
    data = sock.recv(1024)
    response = Ultra.parse(str(data, "ascii"))
    print("R", response.print())

    # ack of session
    # send
    ack = int(response.flags_id[0]) + 1
    session_id = int(response.session_id)
    query = Ultra(O=CONNECTING, I=session_id, f=(ACK, SYN), n=ack)
    print("S", query.print())
    sock.sendto(bytes(str(query), "ascii"), (host, port))
    print("CONNECTED")

    # obtaining range
    # recv
    data = sock.recv(1024)
    response = Ultra.parse(str(data, "ascii"))
    print("R", response.print())

    rangeg = response.response

    # ack o range
    # send
    ack = response.flags_id + 1
    packet = Ultra(O=RANGE, I=session_id, f=ACK, n=ack)
    print("S", packet.print())
    sock.sendto(bytes(str(packet), "ascii"), (host, port))

    ex = False
    while not ex:
        # guess with hit
        # send
        packet = Ultra(O=GUESS, o=randrange(rangeg[0], rangeg[1]), I=session_id, f=PUSH, n=800)
        print("S", packet.print())
        sock.sendto(bytes(str(packet), "ascii"), (host, port))

        # ack
        # recv
        data = sock.recv(1024)
        response = Ultra.parse(str(data, "ascii"))
        print("R", response.print())

        # response
        # recv
        data = sock.recv(1024)
        response = Ultra.parse(str(data, "ascii"))
        print("R", response.print())
        if response.response == "=":
            ex = True

        # ack of response form server
        # send
        packet = Ultra(O=GUESS, I=session_id, f=ACK, n=response.flags_id+1)
        print("S", packet.print())
        sock.sendto(bytes(str(packet), "ascii"), (host, port))


# end
if __name__ == "__main__":
    HOST, PORT = "192.168.1.101", 9999
    args = sys.argv
    host = args[1] if len(args) > 1 else HOST
    port = int(args[2]) if len(args) > 2 else PORT

    client_moc(host, port)
    input("Press ENTER to continue...")
    sys.exit()
