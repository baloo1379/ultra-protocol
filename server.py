import socketserver
import threading
from random import randrange
import Protocol.protocol as proto
import Utils.utils as u


class ThreadedUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global clients
        u.debugger("Handle entered")
        data = str(self.request[0], "ascii")
        cur_thread = threading.current_thread()
        u.debugger("on {} {} wrote:".format(cur_thread.name, self.client_address[0]))
        query = proto.Ultra()
        try:
            query.parse(data)
        except ValueError as err:
            print(err)
        else:
            print(query)
            response = proto.Ultra()
            u.debugger(query.flags)
            if query.flags == (proto.PUSH, proto.SYN):
                # first connect packet from client
                current_session_id = randrange(0, 1024)
                ack = query.flags_id[0] + 1
                u.debugger("connecting", current_session_id, ack)
                response = proto.Ultra(O=query.operation, I=current_session_id, f=(proto.PUSH, proto.ACK, proto.SYN),
                                       n=(randrange(0, 1024), ack))

            s = self.request[1]
            u.debugger("prepared response: ", response)
            response = bytes(str(response), 'ascii')
            s.sendto(response, self.client_address)
        finally:
            u.debugger("Handle exited")








class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    clients = list()
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    server.serve_forever()
    server.shutdown()
    server.server_close()
