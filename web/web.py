from flask import Flask, render_template, jsonify, Response
app = Flask(__name__, static_url_path='/static', static_folder='../static', template_folder='../templates')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from consolelog import *

import json
config = json.load(open("./config.json", "r"))

arena = None
# api_key adds a small amount of obfuscation to the api links but does not provide any security.
# Do not leave the field network open to the public
api_key = config["api_key"]

def Init(_arena):
    global arena
    arena = _arena

def RunWrapper(port, _):
    app.run(port=port, host="0.0.0.0")

@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/displays/main")
def mainDisplay():
    return render_template("main-display.htm")

@app.route("/displays/chroma")
def chromaDisplay():
    return render_template("chroma-display.htm")

@app.route("/control")
def matchControl():
    return render_template("match-control.htm")

@app.route("/scoring")
def score():
    return render_template("scoring.htm")

## API ##
@app.route("/api/key.js")
def apiKey():
    return Response(f"var api_key = '{api_key}';", mimetype="text/javascript")

@app.route("/api/fieldinfo")
def fieldInfo():
    red_score = arena.red_score.points
    blue_score = arena.blue_score.points

    alliance_stations = {}
    for station in arena.alliance_stations:
        alliance_stations[station] = {}

        station_id = station
        station = arena.alliance_stations[station]

        if station.team:
            alliance_stations[station_id]["team"] = {"id": station.team.id}
            
        if station.driverstation_connection:
            alliance_stations[station_id]["driverstation_connection"] = {
                "robot_linked": station.driverstation_connection.robot_linked,
                "radio_linked": station.driverstation_connection.radio_linked,
                "ds_linked": station.driverstation_connection.ds_linked,
                "battery_voltage": station.driverstation_connection.battery_voltage,
                "seconds_since_last_robot_link": station.driverstation_connection.seconds_since_last_robot_link
            }
        
        alliance_stations[station_id]["bypass"] = station.bypass

    return jsonify({
        "scores": {
            "red": red_score,
            "blue": blue_score
        },
        "AllianceStations": alliance_stations,
        "MatchState": arena.match_state,
        "time":round(arena.MatchTimeSec())
        })

@app.route("/api/" + api_key + "/score/blue/<number>")
def blueScore(number):
    global arena
    arena.blue_score.points += int(number)
    return "Done"

@app.route("/api/" + api_key + "/score/red/<number>")
def redScore(number):
    global arena
    arena.red_score.points += int(number)
    return "Done"

@app.route("/api/" + api_key + "/control/startmatch")
def startMatch():
    arena.StartMatch()
    return "Done"

@app.route("/api/" + api_key + "/control/stopmatch")
def stopMatch():
    arena.AbortMatch()
    return "Done"

@app.route("/api/" + api_key + "/control/alliancestation/<station>/<team>")
def allianceStation(station, team):
    return str(arena.AssignTeam(team, station))

@app.route("/api/" + api_key + "/control/bypass/<station>")
def bypass(station):
    if station not in arena.alliance_stations:
        return "Invalid station"
    
    arena.alliance_stations[station].bypass = not arena.alliance_stations[station].bypass
    notice(f"Bypass on station {station} has been set to {arena.alliance_stations[station].bypass}")

    return "Done"