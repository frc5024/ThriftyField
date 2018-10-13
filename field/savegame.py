# For saving game data.

def createCSV(filename: str):
	file = open(filename, "w")
	# Create CSV hedaer
	data = 'Game Number,Game Type,R1,R2,R3,B1,B2,B3,Red Score,Blue Score,Winning Alliance,'
	file.writelines(data)

def writeMatch(filename: str
