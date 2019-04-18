from model.database import Database
from model.team import Team
from field.driverstationconnection import DriverStationConnection, ListenForDsUdpPackets, ListenForDriverstations
from logging import *
from game import matchtiming 

import time
from threading import Thread

arena_loop_period_ms = 10
ds_packet_period_ms = 250
match_end_score_dwell_sec = 3
post_timeout_sec = 4

class MatchState:
    pre_match = 0
    start_match = 1
    warmup_period = 2
    auto_period = 3
    pause_period = 4
    teleop_period = 5
    post_match = 6
    timeout_active = 7
    post_timeout = 8

class AllianceStation:
    driverstation_connection = None
    tcp_conn_thread = None
    astop = False
    estop = False
    bypass = False

    def __init__(self):
        self.team = Team()

class Arena(object):
    database = None
    event_settings = None
    displays = None
    match_aborted = False
    last_ds_packet_time = None
    blue_realtime_score = None
    red_realtime_score = None
    alliance_stations = {}
    tba_client = None
    match_start_time = 0
    last_match_time_sec = 0

    driverstation_listener = None
    driverstation_udp_packet_listener = None

    def __init__(self, db_path):
        self.database = Database(db_path)

        # Set up alliance stations
        self.alliance_stations["R1"] = AllianceStation()
        self.alliance_stations["R2"] = AllianceStation()
        self.alliance_stations["R3"] = AllianceStation()
        self.alliance_stations["B1"] = AllianceStation()
        self.alliance_stations["B2"] = AllianceStation()
        self.alliance_stations["B3"] = AllianceStation()

        self.match_state = MatchState.pre_match

        self.last_match_time = 0
        self.last_match_state = -1

        self.audience_display_mode = "blank"
        self.alliance_station_display_mode = "match"
    
    def Run(self):
        # listen for driverstations
        self.driverstation_listener = Thread(target=ListenForDriverstations, args=(self, None))
        self.driverstation_listener.start()

        # Listen for DS UDP packets
        self.driverstation_udp_packet_listener = Thread(target=ListenForDsUdpPackets, args=(self, None))
        self.driverstation_udp_packet_listener.start()

        notice("Arena has started")
        while True:

            time.sleep(arena_loop_period_ms / 1000)
    
    def GetAssignedAllianceStation(self, team_id: int):
        for station in self.alliance_stations:
            if alliance_stations[station].team != None and alliance_stations[station].team.id == team_id:
                return station
        return ""

    def Update(self):
        auto = False
        enabled = False
        send_ds_packet = False
        match_time_sec = None

        if self.match_state == MatchState.pre_match:
            auto = True
            enabled = False
        elif self.match_state == MatchState.start_match:
            self.match_start_time = time.time()
            self.last_match_time_sec = -1
            auto = True
            self.audience_display_mode = "match"
            self.alliance_station_display_mode = "match"
            # TODO: notify display modes
            self.match_state = MatchState.auto_period
            enabled = True
            send_ds_packet = True
        elif self.match_state == MatchState.auto_period:
            auto = True
            enabled = True
            if match_time_sec >= matchtiming.auto_duration_sec:
                auto = False
                send_ds_packet = True
                self.match_state = MatchState.teleop_period
                enabled = True
        elif self.match_state == MatchState.teleop_period:
            auto = False
            enabled = True
            if match_time_sec >= matchtiming.auto_duration_sec + match.teleop_duration_sec:
                self.match_state = MatchState.post_match
                auto = False
                enabled = False
                send_ds_packet = True
                time.sleep(3)
                self.audience_display_mode = "blank"
                self.alliance_station_display_mode = "logo"
                # TODO: notify display modes
