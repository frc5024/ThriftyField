from flask import Flask
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
	return str([globaldata.scores,globaldata.teams,globaldata.time])

# Start webserver
if __name__ == '__main__':
	app.run(port=int(config["field_api_port"]))