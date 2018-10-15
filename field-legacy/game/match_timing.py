# Source: https://github.com/Team254/cheesy-arena/blob/master/game/match_timing.go

duration = {
  "Warmup" : 3,
	"Auto" : 15,
	"Pause" : 2,
	"Teleop" : 135,
	"Endgame_legnth" : 30
}
def gameLegnth():
	return (duration["Warmup"] + duration["Auto"] + duration["Pause"] + duration["Teleop"])

duration["total"] = gameLegnth()
