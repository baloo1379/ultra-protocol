import socketserver
import threading
from random import randrange
import Protocol.protocol as proto
import Utils.utils as u


class ThreadedUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global clients, clients_ip, range_for_clients
        u.debugger("clients list:", clients)
        u.debugger("Handle entered")
        data = str(self.request[0], "ascii")
        cur_thread = threading.current_thread()
        u.debugger("on {} {} wrote:".format(cur_thread.name, self.client_address[0]))
        ack = 0
        prev_ack = 0
        send = False
        client_address = ("0.0.0.0", 0)
        try:
            query = proto.Ultra.parse(data)
        except ValueError as err:
            print(err)
        else:
            print(query)
            response = proto.Ultra()
            u.debugger(query.flags)
            if query.flags == (proto.PUSH, proto.SYN):
                # first connect packet from client
                current_session_id = randrange(0, 1024)
                push = randrange(0, 1024)
                ack = int(query.flags_id[0]) + 1
                client_address = self.client_address
                clients.append([current_session_id, push])
                clients_ip.update({current_session_id: client_address})
                u.debugger("connecting", current_session_id, ack)
                response = proto.Ultra(O=query.operation, I=current_session_id, f=(proto.PUSH, proto.ACK, proto.SYN),
                                       n=(push, ack))
                send = True
            if query.flags == (proto.ACK, proto.SYN):
                # ack of connection
                send = False
                client_session_id = int(query.session_id)
                ack = int(query.flags_id[0])
                u.debugger(client_session_id, ack)
                try:
                    i = clients.index([client_session_id, ack-1])
                    clients.remove([client_session_id, ack-1])
                except ValueError as err:
                    # client don't exists
                    u.debugger("client don't exists")

                else:
                    u.debugger("client exists and ack ok", i)
                    print("CONNECTED")
                    push = randrange(0, 1024)
                    clients.append([client_session_id, push])
                    # preparing range packet
                    response = proto.Ultra(O=proto.RANGE, o=range_for_clients, I=client_session_id, f=proto.PUSH, n=push)
                    send = True
                    client_address = clients_ip[client_session_id]

            if query.flags == proto.ACK:
                # TODO
                # utworzyć dalej ack i inne możliwości pakietów od klienta

                # ack of range
                client_session_id = int(query.session_id)
                ack = int(query.flags_id[0])
                u.debugger(client_session_id, ack)
                try:
                    i = clients.index([client_session_id, ack-1])
                    # clients.remove([client_session_id, ack-1])
                except ValueError as err:
                    # client don't exists
                    u.debugger("client don't exists")
                else:
                    u.debugger("client exists and ack ok", i)
                # ack of response

            if send:
                s = self.request[1]
                u.debugger("prepared response: ", response)
                response = bytes(str(response), 'ascii')
                s.sendto(response, client_address)
        finally:
            u.debugger("Handle exited")


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    clients = [0, 0]
    clients_ip = {0: ("127.0.0.1", 9999)}
    range_for_clients = (randrange(0, 1024), randrange(0, 1024))
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    server.serve_forever()
    server.shutdown()
    server.server_close()
