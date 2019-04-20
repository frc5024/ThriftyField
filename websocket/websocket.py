import logging
from websocket_server import WebsocketServer
from threading import Thread
import json

config = json.load(open("./config.json", "r"))

server = WebsocketServer(config["websocket_port"], host='0.0.0.0')

def RunWrapper():
    ws_thread = Thread(target=server.run_forever)
    ws_thread.start()
