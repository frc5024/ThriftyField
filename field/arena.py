from model.database import Database

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
    team = None

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
    
    

