import socket
import random
import sys
from Protocol.protocol import *
from Utils.utils import debugger


def client(host, port, client_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, client_port))
    server_adddress = (host, port)

    # connecting
    packet = Ultra(O=CONNECTING, f=(PUSH, SYN), n=random.randrange(0, 2048))
    ack_n = int(packet.flags_id)
    debugger("S", packet.print())
    sock.sendto(bytes(packet.pack(), "ascii"), server_adddress)

    # recv ack and session_id of connecting
    received = sock.recv(1024)
    response = Ultra.parse(str(received, "ascii"))
    debugger("R", response.print())
    if int(response.flags_id[1]) != ack_n+1:
        print("Wrong ack. Quiting")
        debugger(response.flags_id, ack_n)
        return
    else:
        # sending ack of connection
        session_id = response.session_id
        query = Ultra(O=CONNECTING, I=session_id, f=(ACK, SYN), n=int(response.flags_id[0])+1)
        debugger("S", query.print())
        sock.sendto(bytes(query.pack(), "ascii"), server_adddress)
        print("Connected to server")

        # recv of range
        received = sock.recv(1024)
        received = str(received, "ascii")
        received = Ultra.parse(received)
        debugger("R", received.print())
        range = received.response


        # ack of recv range
        query = Ultra(O=received.operation, I=session_id, f=ACK, n=int(received.flags_id) + 1)
        debugger("S", query.print())
        sock.sendto(bytes(query.pack(), "ascii"), server_adddress)
        ac_flag = int(response.flags_id[1])
        print("Please guess number between ", range[0], " and ", range[1])
        # connected and range obtained
        w_flag = True
        while w_flag:
            # guessing
            try:
                st_guess = input("> ")
                st_guess = int(st_guess)
            except ValueError:
                print("Type number")
                continue

            if st_guess > range[0] and st_guess < range[1]:
                push = random.randrange(0, 1024)
                send_guess = Ultra(O=GUESS, o=st_guess, I=session_id, f=PUSH, n=push)
                sock.sendto(bytes(send_guess.pack(), "ascii"), server_adddress)
                debugger(send_guess.print())
            else:
                print("Given number is not from range")
                continue

            data = sock.recv(1024)
            data = Ultra.parse(str(data, "ascii"))
            debugger(ac_flag, data.flags_id)
            if int(data.flags_id) == push+1:
                debugger("otrzymałem poprawnego ack")
            else:
                debugger("niepoprawny ack")


            #recv answer
            received = sock.recv(1024)
            received = str(received, "ascii")
            received = Ultra.parse(received)
            debugger(received.print())
            if received.response == "<":
                print("Too small. Type bigger number.")
            elif received.response == "=":
                print("HIT. Congratulations.")
                w_flag = False
            elif received.response == ">":
                print("Too big. Type smaller number.")

            #ack send
            ack_n = received.flags_id+1
            send_ack = Ultra(O=RESPONSE, I=session_id, f=ACK, n=ack_n)
            debugger(send_ack.print())
            sock.sendto(bytes(send_ack.pack(), "ascii"), server_adddress)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    args = sys.argv
    host = args[1] if len(args) > 1 else HOST
    port = int(args[2]) if len(args) > 2 else PORT
    client_port = int(args[3]) if len(args) > 3 else PORT-1

    client(host, port, client_port)
