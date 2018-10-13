from flask import Flask
from flask import request
import json
import globaldata as globaldata

app = Flask(__name__)

# Load the master config file
with open("./config.json") as conf:
	config = json.load(conf)

@app.route("/")
def index():
	# Return useless message
	return "ThriftyField API Server"

@app.route("/api/score")
def score():
	#return json object
	return str(globaldata.scores)

@app.route("/api/teams/onfield")
def onfield():
	#return json object
	return str(globaldata.teams)

@app.route("/api/gametime")
def gametime():
	#return json object
	return str(globaldata.time)

@app.route("/api/getall")
def getall():
	#return json object
	return str({"scores":globaldata.scores,"teams":globaldata.teams,"time":globaldata.time}).replace("\'", "\"")

@app.route("/admin")
def admin():
	template = open("./field/templates/admin.html", "r").read()
	
	# if b3 in request.args:
	globaldata.teams["red"][0] = request.args.get("r1")
	globaldata.teams["red"][1] = request.args.get("r2")
	globaldata.teams["red"][2] = request.args.get("r3")
	
	globaldata.teams["blue"][0] = request.args.get("b1")
	globaldata.teams["blue"][1] = request.args.get("b2")
	globaldata.teams["blue"][2] = request.args.get("b3")
	return template

# Start webserver
if __name__ == '__main__':
	app.run(port=int(config["field_api_port"]))