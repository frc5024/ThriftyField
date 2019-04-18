from model.database import Database
from model.team import Team
from field.driverstationconnection import DriverStationConnection, ListenForDsUdpPackets, ListenForDriverstations
from logging import *

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

            time.sleep(arena_loop_period_ms)

