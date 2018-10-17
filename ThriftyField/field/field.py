from field import driverstation as dsconn
from threading import Thread
import time

# Config
arenaLoopPeriodMs     = 10
dsPacketPeriodMs      = 250
matchEndScoreDwellSec = 3
postTimeoutSec        = 4

AllianceStation = {
		"id"           : "B1",
		"DsConnection" : "",
		"Estop"        : False,
		"Bypass"       : False,
		"Team"         : ""
}

# Make a class for a field
class Field(object):
	def __init__(self):
		# 2d array of allience stations
		self.alliance_stations = [[AllianceStation("B1"),AllianceStation("B2"),AllianceStation("B3")],[AllianceStation("R1"),AllianceStation("R2"),AllianceStation("R3")]]
		
		# Keep track of who is ready
		self.BlueAllianceReady = False
		self.RedAllianceReady  = True
		
		# Driverstations
		lastDsPacketTime = 0.0

# List of stations
allianceStations = {"B1":AllianceStation,"B2":AllianceStation,"B3":AllianceStation,"R1":AllianceStation,"R2":AllianceStation,"R3":AllianceStation}


def getAssignedStation(team):
	if team == "5024":
		return "B1"
	else:
		return "R1"

# Threads
class FindDS(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		dsconn.listenForDS()
	
	# def stop(self):
	# 	dsconn.running = False
#

def run():
	fDS = FindDS()
	fDS.start()
	
	# Loop
	print("Type EXIT to close")
	while True:
		time.sleep(0.001 * arenaLoopPeriodMs)
			