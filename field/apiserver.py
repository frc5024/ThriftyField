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
	return str({"scores":globaldata.scores,"teams":globaldata.teams,"time":int(globaldata.time), "field":globaldata.field, "enabled":globaldata.game_enabled, "timings":globaldata.timings}).replace("\'", "\"").replace("False", "0").replace("True", "1")

@app.route("/admin", methods=["GET", "POST"])
def admin():
	template = open("./field-legacy/templates/admin.html", "r").read()
	
	if request.method == 'POST':
		# Set the game state
		print(request.form.get("start"))
		if request.form.get("start"):
			print("Enabled game")
			globaldata.game_enabled = True
			# print(globaldata.game_enabled)
			# For resetting clock
			globaldata.firsttick = True
		elif request.form.get("stop"):
			print("stopped game")
			globaldata.game_enabled = False
	
	# if b3 in request.args:
	globaldata.teams["red"][0] = request.args.get("r1")
	globaldata.teams["red"][1] = request.args.get("r2")
	globaldata.teams["red"][2] = request.args.get("r3")
	
	globaldata.teams["blue"][0] = request.args.get("b1")
	globaldata.teams["blue"][1] = request.args.get("b2")
	globaldata.teams["blue"][2] = request.args.get("b3")
	return template

@app.route("/ref", methods=["GET", "POST"])
def ref():
	if request.method == 'POST':
		print(request.form)
		
		# rswitch
		if request.form.get("RL"):
			globaldata.field["switchR"]["state"] = "backward"
		if request.form.get("RC"):
			globaldata.field["switchR"]["state"] = "centre"
		if request.form.get("RR"):
			globaldata.field["switchR"]["state"] = "forward"
			
		if request.form.get("SL"):
			globaldata.field["scale"]["state"] = "backward"
		if request.form.get("SC"):
			globaldata.field["scale"]["state"] = "centre"
		if request.form.get("SR"):
			globaldata.field["scale"]["state"] = "forward"
			
		if request.form.get("BL"):
			globaldata.field["switchB"]["state"] = "backward"
		if request.form.get("BC"):
			globaldata.field["switchB"]["state"] = "centre"
		if request.form.get("BR"):
			globaldata.field["switchB"]["state"] = "forward"
	
	template = open("./field-legacy/templates/ref.html", "r").read()
	
	return template

# Start webserver
if __name__ == '__main__':
	app.run(port=int(config["field_api_port"]), host= '0.0.0.0')