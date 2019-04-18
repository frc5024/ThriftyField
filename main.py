import json

from field.arena import Arena
from logging import *

notice("Loading configuraiton file")
config = json.load(open("./config.json", "r"))

event_db_path = "./event.db"
http_port = 8080

arena = Arena(event_db_path)

arena.Run()