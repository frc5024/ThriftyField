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
	},
	"ownerships":{
		# Can be n,r,or b
		"red_switch":"b",
		"blue_switch":"n",
		"scale":"n"
	}
}

scores = {
	"red":"00",
	"blue":"00"
}

teams = {
	"red":["0000","0000","0000"],
	"blue":["0000","0000","0000"]
}



time = 00
start_time = 00

stopservers = False

game_enabled = False
firsttick = False