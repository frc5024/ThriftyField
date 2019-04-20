import json
from threading import Thread
import time

from field.arena import Arena
from web import web
from consolelog import *

notice("Loading configuraiton file")
config = json.load(open("./config.json", "r"))

event_db_path = "./event.db"
http_port = 8080

if __name__ == "__main__":
    arena = Arena(event_db_path)

    web.Init(arena)
    web_thread = Thread(target=web.RunWrapper, args=(http_port, None))

    # Start webserver and field
    web_thread.start()
    time.sleep(0.5)
    arena.Run()