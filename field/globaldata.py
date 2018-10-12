# All views are from the judges table
field = {
	# State: setup,auto,teleop,estop
	"state":"setup",
	"switchR":{
		"connected":False,
		# State: centre,forward,backward
		"state":"centre"
	},
	"switchB":{
		"connected":False,
		# State: centre,forward,backward
		"state":"centre"
	},
	"scale":{
		"connected":False,
		# State: centre,forward,backward
		"state":"centre"
	},
	"vaultR":{
		"force_count":0,
		"levitate_count":0,
		"boost_count":0,
		"active":[]
	},
	"vaultB":{
		"force_count":0,
		"levitate_count":0,
		"boost_count":0,
		"active":[]
	}
}

scores = {
	"red":0,
	"blue":0
}

teams = {
	"red":[0000,0000,0000],
	"blue":[0000,0000,0000]
}

time = 0.00

stopservers = False