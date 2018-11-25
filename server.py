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
        u.debugger("data:", data)
        packet = proto.Ultra()
        try:
            packet = packet.parse(data)
        except ValueError as err:
            print(err)
        cur_thread = threading.current_thread()

        # response = bytes(str(proto.Ultra(O=proto.CONNECTING, I=)), 'ascii')
        socket = self.request[1]
        print("on {} {} wrote:".format(cur_thread.name, self.client_address[0]))

        # socket.sendto(response, self.client_address)
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
