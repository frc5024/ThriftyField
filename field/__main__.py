import json
import apiserver as api
import globaldata as globaldata
import field as field
import network as network
from datetime import datetime
from threading import Thread
import apiserver as apiserver
from game import match_timing as mt
import logging

globaldata.timings = mt.duration

# Load the master config file
with open("./config.json") as conf:
	config = json.load(conf)

class server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.running = True

	def run(self):
		# log = logging.getLogger('werkzeug')
		# log.disabled = True
		# apiserver.app.logger.disabled = True
		apiserver.app.run(port=int(config["field_api_port"]), host= '0.0.0.0')
	
	def stop(self):
		self.running = False


# Start api server
svr = server()



# Outline:
# Start apiserv
# init:
# start serial
# find arduinos
# report findings to globaldata

def main():
	# Start hardware
	fci = field.init()
	network.init()
	
	running = not globaldata.stopservers
	
	def writeStates(states):
		globaldata.field["switchR"]["connected"] = states["rswitch"][1]
		globaldata.field["switchR"]["state"] = states["rswitch"][0]
		
		globaldata.field["scale"]["connected"] = states["scale"][1]
		globaldata.field["scale"]["connected"] = states["scale"][1]
		
		globaldata.field["switchB"]["connected"] = states["bswitch"][1]
		globaldata.field["switchB"]["state"] = states["bswitch"][0]
		
	
	while running:
		if globaldata.game_enabled:
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
		
		# Get states of game pieces even if game is stopped
		## CURRENTLY REPLACED BY WEB INTERFACE
		# states = field.getStates(fci)
		# writeStates(states)
		# globaldata.score = calcscore(states, globaldata.score)
		# globaldata.time =

if __name__ == '__main__':
	svr.start()
	main()
	field.close(fci)
	print("Goodbye")
	exit(0)