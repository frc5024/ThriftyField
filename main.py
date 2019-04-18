import json
from threading import Thread

import web

print("Loading configuraiton file")
config = json.load(open("./config.json", "r"))

print("Preparing webservers")
admin_panel = web.AdminWebserver(config["administration"]["webserver_port"])
scoring_panel = web.ScoringWebserver(config["scoring"]["webserver_port"])

# Start the webservers
print("Starting webservers")
admin_panel.Serve()
scoring_panel.Serve()