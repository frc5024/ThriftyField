import json

def NotifyAll(server, arena):
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

    response = json.dumps({
        "scores": {
            "red": red_score,
            "blue": blue_score
        },
        "AllianceStations": alliance_stations,
        "MatchState": arena.match_state,
        "time": round(arena.MatchTimeSec()),
        "sound": arena.current_sound
        })
    
    # Reset arena sound
    arena.current_sound = None
    
    server.send_message_to_all(response)