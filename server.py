import socketserver
import threading
import socket
import sys
from random import randrange
from Protocol.protocol import *
from Utils.utils import debugger


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
        global clients_list, clients_ip_list, range_for_clients, target_for_clients
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

                # creating session_id ,push_id, and calculate ack
                current_session_id = randrange(0, 1024)
                debugger("created session_id", current_session_id)
                push = randrange(0, 1024)
                ack = data.flags_id + 1

                # saving session_id with ip_address and lat push_id
                # client_address = self.client_address
                clients_list.update({current_session_id: push})
                clients_ip_list.update({current_session_id: client_address})

                response = Ultra(O=data.operation, I=current_session_id, f=(PUSH, ACK, SYN), n=(push, ack))
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
                        push = randrange(0, 1024)
                        clients_list.update({client_session_id: push})
                        # preparing range packet
                        response = Ultra(O=RANGE, o=range_for_clients, I=client_session_id, f=PUSH, n=push)
                        client_address = clients_ip_list[client_session_id]
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
                    if number == target_for_clients:
                        # hit - koniec gry
                        sign = "="
                    else:
                        if number < target_for_clients:
                            # send <
                            sign = "<"
                        else:
                            # send >

                            sign = ">"
                    push = randrange(0, 1024)
                    clients_list.update({client_session_id: push})
                    response = Ultra(O=data.operation, o=sign, I=client_session_id, f=PUSH, n=push)
                    send(self.request[1], response, client_address)

        finally:
            debugger("=== Handle exited ===", "\n")

    def finish(self):
        debugger("===== Tables ======")
        debugger(clients_list)
        debugger(clients_ip_list)
        debugger("===================", "\n")


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class ThreadedClose(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        exit_condition = input()
        if exit_condition == "exit":
            print("Closing...")
            self.s.shutdown()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    args = sys.argv
    host = args[1] if len(args) > 1 else HOST
    port = int(args[2]) if len(args) > 2 else PORT

    clients_list = {}
    clients_ip_list = {}
    a = randrange(0, 512)
    b = randrange(513, 1024)
    target_for_clients = randrange(a, b)
    range_for_clients = (a, b)
    print("Target:", target_for_clients)
    print("Range:", range_for_clients)

    # starting multithread server
    server = ThreadedUDPServer((host, port), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    close_thread = ThreadedClose(server)

    server_thread.daemon = True
    close_thread.daemon = True
    server_thread.start()
    close_thread.start()

    print("Server IP: ", server.server_address[0], "at port", server.server_address[1])
    print("Server loop running in thread:", server_thread.name)

    server.serve_forever()

    print("Server closed")
    server.server_close()
