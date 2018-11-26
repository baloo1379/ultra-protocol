import socket
from random import randrange
import Protocol.protocol as proto
from time import sleep
import Utils.utils as u


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, 9998))
    counter = 1

    # first
    data = s.recvfrom(1024)
    query = proto.Ultra.parse(data[0].decode("ascii"))
    print(f"\n{counter} from client:\n"+str(query))
    counter += 1

    # second
    current_session_id = randrange(0, 1024)
    push = randrange(0, 1024)
    ack = int(query.flags_id[0]) + 1
    response = proto.Ultra(O=query.operation, I=current_session_id,
                           f=(proto.PUSH, proto.ACK, proto.SYN),
                           n=(push, ack))
    sleep(0.5)
    print(f"\n{counter} to client:\n"+str(response))
    counter += 1
    s.sendto(bytes(str(response), "ascii"), (HOST, PORT))

    # third
    data = s.recvfrom(1024)
    query = proto.Ultra.parse(data[0].decode("ascii"))
    print(f"\n{counter} from client:\n" + str(query))
    counter += 1

    # fourth
    push = randrange(0, 1024)
    range_for_clients = (randrange(0, 1024), randrange(0, 1024))
    response = proto.Ultra(O=proto.RANGE, o=range_for_clients, I=current_session_id, f=proto.PUSH, n=push)
    sleep(0.5)
    print(f"\n{counter} to client:\n" + str(response))
    counter += 1
    s.sendto(bytes(str(response), "ascii"), (HOST, PORT))

    # fifth
    # tu takie bloki sobie rób odbioru i wysyłki i dostosuj jak potrzebujesz.
    # na razie nie rób tu logiki, że sprawdzanie ack itd, jedynie weź wklej linijkę 17 (ack)
    # żeby serwer dobre ack ci odsyłał jak w cliencie będziesz sprawdzał
    data = s.recv(1024)
    query = proto.Ultra.parse(data.decode("ascii"))
    print(f"\n{counter} from client:\n" + str(query))
    counter += 1

    # push = randrange(0, 1024)
    # range_for_clients = (randrange(0, 1024), randrange(0, 1024))
    # response = proto.Ultra(O=proto.RANGE, o=range_for_clients, I=current_session_id, f=proto.PUSH, n=push)
    # sleep(0.5)
    # print(f"\n{counter} to client:\n" + str(response))
    # counter += 1
    # s.sendto(bytes(str(response), "ascii"), (HOST, PORT))
    #
    # # fourth
    # data = s.recv(1024)
    # query = proto.Ultra.parse(data.decode("ascii"))
    # print(f"\n{counter} from client:\n" + str(query))
    # counter += 1


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server()




