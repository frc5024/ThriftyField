import json
import apiserver as api
import globaldata as globaldata


# Load the master config file
with open("./config.json") as conf:
	config = json.load(conf)

# Outline:
# Start apiserv
# init:
# start serial
# find arduinos
# report findings to globaldata

field.init()
network.init()

running = not globaldata.stopservers

while running:
	states = field.getStates()
	globaldata.writeStates(states)
	globaldata.score = calcscore(states, globaldata.score)
	globaldata.time =

field.close()
print("Goodbye")
exit(0)