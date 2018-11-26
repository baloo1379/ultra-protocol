import socket
import random
import Protocol.protocol as proto
import Utils.utils as u


HOST, PORT = "localhost", 9998


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, 9999))

    # connecting
    packet = proto.Ultra(O=proto.CONNECTING, f=(proto.PUSH, proto.SYN), n=random.randrange(0, 2048))
    ack_n = int(packet.flags_id[0]) + 1
    print(packet)
    sock.sendto(bytes(str(packet), "ascii"), (HOST, PORT))

    # recv ack and session_id of connecting
    received = sock.recv(1024)
    response = proto.Ultra.parse(str(received, "ascii"))
    print(response)
    if int(response.flags_id[1]) != ack_n:
        print("Wrong ack. Quiting")
        u.debugger(response.flags_id[1], ack_n)
        return
    else:
        # sending ack of connection
        session_id = response.session_id
        u.debugger("session_id", session_id)
        query = proto.Ultra(O=proto.CONNECTING, I=session_id, f=(proto.ACK, proto.SYN), n=int(response.flags_id[0])+1)
        sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))

        # recv of range
        received = sock.recv(1024)
        received = str(received, "ascii")
        received = proto.Ultra.parse(received)
        print(received)

        # ack of recv range
        query = proto.Ultra(O=received.operation, I=session_id, f=proto.ACK, n=int(response.flags_id[0]) + 1)
        sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))

        #while
            # first guess


if __name__ == "__main__":
    client()
