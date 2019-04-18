import requests

tba_base_url = "https://www.thebluealliance.com"
tba_auth_key = requests.get("https://api.retrylife.ca/auth/tba").json()["key"]
avatars_dir = "static/img/avatars"

class TbaTeam:
    number = 0
    name = ""
    nickname = ""
    city = ""
    rookie_year = 0

def GetTeam(number: int):
    resp = requests.get(tba_base_url + f"/api/v3/team/frc{number}", headers={"X-TBA-Auth-Key": tba_auth_key}).json()

    team = TbaTeam()
    team.number = number
    team.name = resp["name"]
    team.nickname = resp["nickname"]
    team.city = resp["city"]
    team.rookie_year = resp["rookie_year"]

    return team

def GetRobotName(number: int, year: int):
    resp = requests.get(tba_base_url + f"/api/v3/team/frc{number}/robots", headers={"X-TBA-Auth-Key": tba_auth_key}).json()

    for robot in resp:
        if robot["year"] == year:
            return robot["robot_name"]
    
    return ""