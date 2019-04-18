from .database import Database

elim_round_names = {1: "F", 2: "SF", 4: "QF", 8: "EF"}

class Match:
    id = 0
    type = ""
    display_name = ""
    time = 0
    elim_round = 0
    elim_group = 0
    elim_instance = 0
    red1 = 0
    red1_is_surrogate = False
    red2 = 0
    red2_is_surrogate = False
    red3 = 0
    red3_is_surrogate = False
    blue1 = 0
    blue1_is_surrogate = False
    blue2 = 0
    blue2_is_surrogate = False
    blue3 = 0
    blue3_is_surrogate = False
    status = ""
    started_at = 0
    score_committed_ad = 0
    winner = ""
    gsm = ""

    def Save(self, database: Database):
        database.data["matchMap"].append(self)


