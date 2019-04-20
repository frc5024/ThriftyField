from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/static', static_folder='../static', template_folder='../templates')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

arena = None

def Init(_arena):
    global arena
    arena = _arena 

def RunWrapper(port, _):
    app.run(port=port)

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
def maychControl():
    return render_template("match-control.htm")

## API ##
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
            alliance_stations[station_id]["team"] = {"id":5024}#{"id": station.team.id}
            
        if station.driverstation_connection:
            alliance_stations[station_id]["driverstation_connection"] = {
                "robot_linked": station.driverstation_connection.robot_linked,
                "radio_linked": station.driverstation_connection.radio_linked,
                "ds_linked": station.driverstation_connection.ds_linked,
                "battery_voltage": station.driverstation_connection.battery_voltage,
                "seconds_since_last_robot_link": station.driverstation_connection.seconds_since_last_robot_link
            }

    return jsonify({
        "scores": {
            "red": red_score,
            "blue": blue_score
        },
        "AllianceStations": alliance_stations
        })