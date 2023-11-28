# Aerics
A networking library written Python for online games.

## Getting Started
1) Install Python
2) Open cmd/terminal and type:

```
pip install Aerics
```

## Examples
# Creating a server
``` python
import aerics, sys

def main(argv):
    server = aerics.Server("localhost", 5656)

    @server.event
    def setup(globals):
        pass

    # @server.event
    # def update():
    #     pass

    @server.event
    def on_connection(connection, address, id, clients, globals):
        print("New connection")
        return {"x" : 0, "y" : 0}

    @server.event
    def on_disconnection(connection, address, id, clients, globals):
        print(f"Client {id} disconnected")

    @server.event
    def on_recv(connection, address, id, clients, globals, data):
        data = data.split(",")

        if data[0] == "move":
            clients[id]["x"], clients[id]["y"] = int(data[1]), int(data[2])
            return clients

        if data[0] == "get_id":
            return id

        if data[0] == "close":
            server.disconnect(connection)
            return None

    server.listen()
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

# Creating a client
``` python
import forges, aerics, sys

class Window(forges.Window):
    def __init__(self):
        super(Window, self).__init__()

        self.client = aerics.Client("localhost", 5656)
        self.client.connect()
        self.client.send("get_id")
        self.id = self.client.recv()
        self.clients = []

        self.player = forges.prefabs.TopViewController()

    def update(self):
        self.client.send(f"move,{self.player.x},{self.player.y}")
        clients = self.client.recv()
        del clients[self.id]

        while len(clients) != len(self.clients):
            if len(clients) < len(self.clients):
                self.clients[0].destroy()
                self.clients.pop(0)

            else:
                self.clients.append(forges.Entity(width = 50, height = 100))

        for index, i in enumerate(clients):
            self.clients[index].x, self.clients[index].y = clients[i]["x"], clients[i]["y"]

def main(argv):
    window = Window()
    forges.run()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
