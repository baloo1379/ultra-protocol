import socketserver
import threading
import Protocol
import Utils


class ThreadedUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data.upper()), 'ascii')
        socket = self.request[1]
        print("on {} {} wrote:".format(cur_thread.name, self.client_address[0]))
        print(data.decode("ascii"))
        socket.sendto(response, self.client_address)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    server.serve_forever()
    server.shutdown()
    server.server_close()




