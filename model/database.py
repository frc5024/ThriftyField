import pickle
import os

backups_dir = "db/backups"
migrations_dir = "db/migrations"

base_dir = "."

class Database:
    data = {
        "eventSettingsMap" : {},
        "matchMap"         : [],
        "matchResultMap "  : {},
        "rankingMap"       : {},
        "teamMap"          : {},
        "allianceTeamMap"  : {},
        "lowerThirdMap"    : {},
        "sponsorSlideMap"  : {},
        "scheduleBlockMap" : {}
    }

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            self.data = pickle.load(open(path, "rb"))
    
    def close(self):
        pickle.dump(self.data, open(self.path, "wb"))
    
    


