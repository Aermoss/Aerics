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

def on_connection(connection, address, id, clients, globals):
    return {"x" : 0, "y" : 0}

def on_disconnection(connection, address, id, clients, globals):
    print("Disconnect")

def on_recv(connection, address, id, clients, globals, data):
    data = data.split(",")

    if data[0] == "move":
        clients[id]["x"], clients[id]["y"] = data[1], data[2]
        return clients

    if data[0] == "close":
        server.disconnect(connection)
        return None

if __name__ == "__main__":
    server = Server("localhost", 5656)
    server.listen()
```

# Creating a client
``` python
from aerforge import *
from aerics import *

def update():
    client.send(f"move,{player.x},{player.y}")
    players = client.recv()

    for i in players:
        forge.draw(width = 50, height = 100, x = int(players[i]["x"]), y = int(players[i]["y"]))

if __name__ == "__main__":
    forge = Forge()
    
    client = Client("localhost", 5656)
    client.connect()

    player = prefabs.TopViewController(forge)
    player.visible = False

    forge.run()
```