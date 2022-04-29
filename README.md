# Aerics
A networking library for multiplayer games.

## Getting Started
1) Install Python
2) Open cmd/terminal and type:

```
pip install Aerics
```

## Examples
# Creating a server
``` python
from aerics import *

server = Server("localhost", 5656)

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
        clients[id]["x"], clients[id]["y"] = data[1], data[2]
        return clients

    if data[0] == "close":
        server.disconnect(connection)
        return None

server.listen()
```

# Creating a client
``` python
from aerforge import *
from aerics import *

import sys

def main(argv):
    global forge, client, player

    forge = Forge()
    
    client = Client("localhost", 5656)
    client.connect()

    player = prefabs.TopViewController(forge)
    player.visible = False

    @forge.event
    def update():
        client.send(f"move,{player.x},{player.y}")
        players = client.recv()

        for i in players:
            forge.draw(width = 50, height = 100, x = int(players[i]["x"]), y = int(players[i]["y"]))

    forge.run()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
