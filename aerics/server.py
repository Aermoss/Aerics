import socket
import threading
import pickle

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
        self.functions = {}

    def event(self, func):
        self.functions[func.__name__] = func

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

        if "setup" in self.functions:
            self.functions["setup"](self.globals)

        if "update" in self.functions:
            thread = threading.Thread(target = self.update_handler, args = [])
            thread.start()

        id = 0

        while not self.destroyed:
            connection, address = self.server.accept()

            thread = threading.Thread(target = self.handler, args = [connection, address, id])
            thread.start()

            id += 1

    def update_handler(self):
        while True:
            self.functions["update"](self.clients, self.globals)

    def handler(self, connection, address, id):
        if not self.destroyed:
            if "on_connection" in self.functions:
                data = self.functions["on_connection"](connection, address, id, self.clients, self.globals)

                if data == None:
                    self.clients[id] = {}

                else:
                    self.clients[id] = data

            else:
                print("Warning: server does not have any on_connection functions")
                self.clients[id] = {}

        while not self.destroyed:
            data = connection.recv(self.recv_size)

            if not data:
                break

            else:
                if self.pickle:
                    data = pickle.loads(data)

                reply = None

                if "on_recv" in self.functions:
                    reply = self.functions["on_recv"](connection, address, id, self.clients, self.globals, data)

                else:
                    print("Warning: server does not have any on_recv functions")

                if reply == None:
                    break

                if self.pickle:
                    reply = pickle.dumps(reply)

                connection.send(reply)

        if not self.destroyed:
            connection.close()
            del self.clients[id]

        if "on_disconnection" in self.functions:
            reply = self.functions["on_disconnection"](connection, address, id, self.clients, self.globals)