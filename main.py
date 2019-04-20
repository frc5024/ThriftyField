import json
from threading import Thread
import time

from field.arena import Arena
from web import web
from websocket import websocket
from consolelog import *

notice("Loading configuraiton file")
config = json.load(open("./config.json", "r"))

event_db_path = "./event.db"
http_port = config["webserver_port"]

if __name__ == "__main__":
    arena = Arena(event_db_path, websocket.server)

    web.Init(arena)
    web_thread = Thread(target=web.RunWrapper, args=(http_port, None))

    # Start webserver and field
    websocket.RunWrapper()
    time.sleep(0.2)
    web_thread.start()
    time.sleep(0.5)
    notice(f"Web application is avalibble on port {http_port}")
    arena.Run()