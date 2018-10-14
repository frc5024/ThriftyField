import json
import apiserver as api
import globaldata as globaldata
import field as field
import network as network
from datetime import datetime
from threading import Thread
import apiserver as apiserver
from game import match_timing as mt

globaldata.timings = mt.duration

# Load the master config file
with open("./config.json") as conf:
	config = json.load(conf)

class server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.running = True

	def run(self):
		apiserver.app.run(port=int(config["field_api_port"]), host= '0.0.0.0')
	
	def stop(self):
		self.running = False


# Start api server
svr = server()
svr.start()

# Outline:
# Start apiserv
# init:
# start serial
# find arduinos
# report findings to globaldata

# Start hardware
field.init()
network.init()

running = not globaldata.stopservers


while running:
	if globaldata.game_enabled:
		
		# print("tick")
		# Set up the clock
		curr_time = datetime.now()
		if globaldata.firsttick:
			globaldata.firsttick = False
			globaldata.starttime = int(curr_time.strftime("%s"))
		
		# set the time
		globaldata.time = int(curr_time.strftime("%s")) - globaldata.starttime
		
		# When the game hits its time limit, do this:
		if str(globaldata.time) == str(mt.duration["total"]):
			globaldata.game_enabled = False
			
	# states = field.getStates()
	# globaldata.writeStates(states)
	# globaldata.score = calcscore(states, globaldata.score)
	# globaldata.time =

# field.close()
print("Goodbye")
exit(0)