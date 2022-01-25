import socket
import pickle

class Client:
    def __init__(self, ip, port, recv_size = 1024, pickle = True):
        self.ip = ip
        self.port = port
        self.recv_size = recv_size
        self.pickle = pickle

        self.destroyed = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if not self.destroyed:
            self.client.connect((self.ip, self.port))

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        
    def send(self, data):
        if not self.destroyed:
            if self.pickle:
                data = pickle.dumps(data)
            
            self.client.send(data)

    def recv(self):
        if not self.destroyed:
            data = self.client.recv(self.recv_size)

            if self.pickle:
                data = pickle.loads(data)

            return data