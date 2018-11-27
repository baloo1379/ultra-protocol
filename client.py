import socket
import random
from Protocol.protocol import *
from Utils.utils import debugger


HOST, PORT = "localhost", 9999


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT-1))

    # connecting
    packet = Ultra(O=CONNECTING, f=(PUSH, SYN), n=random.randrange(0, 2048))
    ack_n = int(packet.flags_id)
    debugger("S", packet.print())
    sock.sendto(bytes(str(packet), "ascii"), (HOST, PORT))

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
        sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
        print("CONNECTED")

        # recv of range
        received = sock.recv(1024)
        received = str(received, "ascii")
        received = Ultra.parse(received)
        debugger("R", received.print())
        range = received.response


        # ack of recv range
        query = Ultra(O=received.operation, I=session_id, f=ACK, n=int(received.flags_id) + 1)
        debugger("S", query.print())
        sock.sendto(bytes(str(query), "ascii"), (HOST, PORT))
        ac_flag = int(response.flags_id[1])

        # connected and range obtained
        w_flag = True
        while(w_flag == True):
                # first guess
            print("Server drew number from range ", range)
            st_guess = input()
            push = random.randrange(0, 1024)
            send_guess = Ultra(O=GUESS, o=st_guess, I=session_id , f= PUSH, n=push)
            sock.sendto(bytes(str(send_guess), "ascii"), (HOST, PORT))
            debugger(send_guess.print())
            #recv ack

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
                print("Drew number is bigger than you gave")
            elif received.response == "=":
                print("Congratulations")
                w_flag = False
            elif received.response == ">":
                print("Drew number is smaller than you gave")

            #ack send
            ack_n = received.flags_id+1
            send_ack = Ultra(O = RESPONSE, I = session_id, f=ACK, n=ack_n)
            debugger(send_ack.print())
            sock.sendto(bytes(str(send_ack), "ascii"), (HOST,PORT))



if __name__ == "__main__":
    client()
