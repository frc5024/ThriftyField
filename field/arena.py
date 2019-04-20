from model.database import Database
from model.team import Team
from field.driverstationconnection import DriverStationConnection, ListenForDsUdpPackets, ListenForDriverstations, SignalMatchStart
from consolelog import *
from game import matchtiming
from game.matchstate import MatchState
from game.score import Score
from websocket.notifiers import NotifyAll

import time
from threading import Thread

arena_loop_period_ms = 10
ds_packet_period_ms = 250
match_end_score_dwell_sec = 3
post_timeout_sec = 4

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
    last_ds_packet_time = 0
    blue_realtime_score = 0
    red_realtime_score =0
    alliance_stations = {}
    tba_client = None
    match_start_time = 0
    last_match_time_sec = 0
    match_time_sec = 0

    red_score = Score()
    blue_score = Score()

    current_sound = None
    

    driverstation_listener = None
    driverstation_udp_packet_listener = None

    def __init__(self, db_path, ws_server):
        self.database = Database(db_path)
        self.ws = ws_server

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
            self.Update()
            time.sleep(arena_loop_period_ms / 1000)
    
    def GetAssignedAllianceStation(self, team_id: int):
        for station in self.alliance_stations:
            if alliance_stations[station].team != None and alliance_stations[station].team.id == team_id:
                return station
        return ""

    def Update(self):
        # print("updating")
        auto = False
        enabled = False
        send_ds_packet = False
        match_time_sec = self.MatchTimeSec()

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
            self.current_sound = "auto"

        elif self.match_state == MatchState.auto_period:
            auto = True
            enabled = True
            if match_time_sec >= matchtiming.auto_duration_sec:
                auto = False
                send_ds_packet = True
                self.match_state = MatchState.teleop_period
                enabled = True
                self.current_sound = "teleop"

        elif self.match_state == MatchState.teleop_period:
            auto = False
            enabled = True
            if match_time_sec >= matchtiming.auto_duration_sec + matchtiming.teleop_duration_sec:
                self.match_state = MatchState.pre_match
                auto = False
                enabled = False
                send_ds_packet = True
                self.current_sound = "matchend"
                time.sleep(3)
                self.audience_display_mode = "blank"
                self.alliance_station_display_mode = "logo"
                # TODO: notify display modes
                

        # TODO: match time notifier
        NotifyAll(self.ws, self)

        self.last_match_time = match_time_sec
        self.last_match_state = self.match_state

        if send_ds_packet or self.last_ds_packet_time >= ds_packet_period_ms:
            self.SendDsPacket(auto, enabled)
    
    def MatchTimeSec(self):
        if self.match_state == MatchState.pre_match or self.match_state == MatchState.start_match:
            return 0
        return time.time() - self.match_start_time
    
    def SendDsPacket(self, auto: bool, enabled: bool):
        for station in self.alliance_stations:
            station = self.alliance_stations[station]

            dsconn = station.driverstation_connection
            if dsconn != None:
                dsconn.auto = auto
                dsconn.enabled = enabled and not station.estop and not station.bypass
                dsconn.estop = station.estop
                dsconn.Update()
    
    def CheckCanStartMatch(self):
        if self.match_state != MatchState.pre_match:
            return "Cannot start match while there is a match in progress or with results still pending"
    
    def AssignTeam(self, team_id: int, station: str):
        if station not in self.alliance_stations:
            return "Invalid alliance station"
        
        dsconn = self.alliance_stations[station].driverstation_connection
        
        if dsconn != None and dsconn.team_id == team_id:
            return None
        
        if dsconn != None:
            dsconn.Close()
            self.alliance_stations[station].team = None
            self.alliance_stations[station].driverstation_connection = None
        
        if team_id == 0:
           self.alliance_stations[station].team = None
           return None
        
        team = Team()
        team.id = team_id
        self.alliance_stations[station].team = team

        notice(f"Team {team_id} has been assigned to station {station}")
        return None
    
    def ResetMatch(self):
        if self.match_state != MatchState.pre_match:
            return "Cannot reset a match while it is in progress"
        
        self.match_state = MatchState.pre_match
        self.match_aborted = False
        self.alliance_stations["R1"].bypass = False
        self.alliance_stations["R2"].bypass = False
        self.alliance_stations["R3"].bypass = False
        self.alliance_stations["B1"].bypass = False
        self.alliance_stations["B2"].bypass = False
        self.alliance_stations["B3"].bypass = False
    
    def AbortMatch(self):
        if self.match_state == MatchState.pre_match:
            return "Cannot abort a match that is not running"
        
        self.match_state = MatchState.pre_match
        self.match_aborted = True
        self.current_sound = "abort"
        warn("Match aborted")
    
    def StartMatch(self):
        for station in self.alliance_stations:
            station = self.alliance_stations[station]

            if station.driverstation_connection != None:
                dsconn = station.driverstation_connection
                SignalMatchStart(dsconn)

                if station.team != None and not station.team.has_connected and dsconn.robot_linked:
                    station.team.has_connected = True
        
        self.match_state = MatchState.start_match
        notice("Match has been started")
