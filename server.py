import socketserver
import threading
import socket
import sys
from random import randrange
from Protocol.protocol import *
from Utils.utils import debugger


DEBUG = True
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def user_exists(s_id: int):
    try:
        clients_list[s_id]
    except KeyError as err:
        # client don't exists
        debugger("client don't exists", err)
        return False
    else:
        return True


def check_ack(s_id: int, ack: int):
    try:
        c_ack = clients_list[s_id]
    except KeyError as err:
        # client don't exists
        debugger("client don't exists", err)
        return False
    else:
        if c_ack == ack-1:
            return True
        else:
            return False


def send(s: socket, response: Ultra, address: tuple):
    debugger("prepared response:".upper())
    debugger(response.print())
    response = bytes(response.pack(), 'ascii')
    s.sendto(response, address)


class ThreadedUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        debugger("--- Handle entered ---")
        global clients_list, clients_state_list, range_for_clients, target_for_clients, waiting_for_players, players, \
            won_player, game_end
        client_address = self.client_address
        raw_data = str(self.request[0], "ascii")
        cur_thread = threading.current_thread()
        try:
            data = Ultra.parse(raw_data)
        except ValueError as err:
            debugger("parsing error:", err)
        else:
            debugger(f"on {cur_thread.name} {client_address[0]} wrote:")
            debugger("RECV DATA:")
            debugger(data.print())

            # recognizing by flags
            if data.flags == (PUSH, SYN):
                # first connect from client
                if waiting_for_players:
                    # creating session_id ,push_id, and calculate ack
                    current_session_id = randrange(0, 1024)
                    debugger("created session_id", current_session_id)
                    push = randrange(0, 1024)
                    ack = data.flags_id + 1

                    # saving session_id with ip_address and lat push_id
                    client_address = self.client_address
                    clients_list.update({current_session_id: push})
                    # clients_state_list.update({current_session_id: CONNECTING})

                    response = Ultra(O=data.operation, o=players, I=current_session_id, f=(PUSH, ACK, SYN), n=(push, ack))
                    send(self.request[1], response, client_address)
                else:
                    #too late
                    push = randrange(0, 1024)
                    ack = data.flags_id + 1
                    response = Ultra(O=data.operation, o="rejected", f=(PUSH, ACK, SYN), n=(push, ack))
                    send(self.request[1], response, client_address)

            if data.flags == (ACK, SYN):
                # ack of connection
                # checking recv session_id and ack
                client_session_id = data.session_id
                ack = data.flags_id
                if not user_exists(client_session_id):
                    debugger("wrong session_id", client_session_id)
                    return
                else:
                    if not check_ack(client_session_id, ack):
                        debugger("wrong ack", ack)
                        return
                    else:
                        debugger("client exists and ack ok")
                        print("CONNECTED WITH", client_session_id)
                        players += 1
                        push = randrange(0, 1024)
                        clients_list.update({client_session_id: push})
                        # preparing range packet
                        while waiting_for_players:
                            pass
                        response = Ultra(O=RANGE, o=range_for_clients, I=client_session_id, f=PUSH, n=push)
                        send(self.request[1], response, client_address)

            if data.flags == ACK:
                # general ack
                debugger("Entered ACK")
                client_session_id = int(data.session_id)
                ack = data.flags_id
                debugger(client_session_id, ack)
                if not user_exists(client_session_id):
                    debugger("client don't exists")
                    return
                else:
                    if not check_ack(client_session_id, ack):
                        debugger("wrong ack", ack)
                        return
                    else:
                        debugger("client exists and ack ok")

            if data.flags == PUSH:
                # client guess
                client_session_id = int(data.session_id)
                ack = data.flags_id
                if not user_exists(client_session_id):
                    debugger("client don't exists")
                    return
                else:
                    # send ack
                    response = Ultra(O=data.operation, I=client_session_id, f=ACK, n=ack+1)
                    send(self.request[1], response, client_address)

                    # send response
                    number = int(data.response)
                    if not game_end:
                        if number == target_for_clients:
                            # hit - koniec gry
                            game_end = True
                            sign = "win"
                            won_player = client_session_id
                            print("Player", client_session_id, "won")
                        else:
                            if number < target_for_clients:
                                # send <
                                sign = "<"
                            else:
                                # send >

                                sign = ">"
                    else:
                        sign = "lose:"+str(won_player)

                    push = randrange(0, 1024)
                    clients_list.update({client_session_id: push})
                    response = Ultra(O=data.operation, o=sign, I=client_session_id, f=PUSH, n=push)
                    send(self.request[1], response, client_address)

        finally:
            debugger("=== Handle exited ===", "\n")

    def finish(self):
        debugger("===== Tables ======")
        debugger(clients_list)
        debugger(clients_state_list)
        debugger("===================", "\n")


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    daemon_threads = True


class ThreadedClose(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        exit_condition = input()
        if exit_condition == "exit":
            print("Closing...")
            self.s.shutdown()


class GameStart(threading.Thread):

    def run(self):
        global waiting_for_players
        debugger("GameStart thread\n")
        # print("Time to close room:")
        el = 0
        while True:
            # print(10-el, "s ", end="\r")
            time.sleep(1)
            if el >= 10:
                print("Time is up. Room closed")
                waiting_for_players = False
                return
            el += 1


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    args = sys.argv
    host = args[1] if len(args) > 1 else HOST
    port = int(args[2]) if len(args) > 2 else PORT

    clients_list = {}
    clients_state_list = {}
    a = randrange(0, 512)
    b = randrange(513, 1024)
    target_for_clients = randrange(a, b)
    range_for_clients = (a, b)
    connect_time = 10
    waiting_for_players = True
    players = 0
    won_player = 0
    game_end = False
    print("Target:", target_for_clients)
    print("Range:", range_for_clients)

    # starting multithread server
    server = ThreadedUDPServer((host, port), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    close_thread = ThreadedClose(server)
    connecting_thread = GameStart()

    server_thread.daemon = True
    close_thread.daemon = True
    connecting_thread.daemon = True

    server_thread.start()
    print("Server IP: ", server.server_address[0], "at port", server.server_address[1])
    print("Server loop running in thread:", server_thread.name)

    close_thread.start()

    print("Clients have 10 seconds to connect")
    connecting_thread.start()

    server.serve_forever()

    print("Server closed")
    server.server_close()
