import socket
import threading
import pickle

import __main__

class Server:
    def __init__(self, ip, port, recv_size = 1024, pickle = True):
        self.ip = ip
        self.port = port
        self.recv_size = recv_size
        self.pickle = pickle

        self.destroyed = False

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))

        self.clients = {}
        self.globals = {}

    def disconnect(self, connection):
        if not self.destroyed:
            connection.close()

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()

    def listen(self, max = 20):
        if not self.destroyed:
            self.server.listen(max)

        id = 0

        while not self.destroyed:
            connection, address = self.server.accept()

            thread = threading.Thread(target = self.handler, args = [connection, address, id])
            thread.start()

            id += 1

    def handler(self, connection, address, id):
        if not self.destroyed:
            self.clients[id] = __main__.on_connection(connection, address, id, self.clients, self.globals)

        while not self.destroyed:
            data = connection.recv(self.recv_size)

            if not data:
                break

            else:
                if self.pickle:
                    data = pickle.loads(data)

                reply = __main__.on_recv(connection, address, id, self.clients, self.globals, data)

                if reply == None:
                    break

                if self.pickle:
                    reply = pickle.dumps(reply)

                connection.send(reply)

        if not self.destroyed:
            connection.close()
            del self.clients[id]

        __main__.on_disconnection(connection, address, id, self.clients, self.globals)