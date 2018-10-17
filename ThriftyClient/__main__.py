"""Client program to be run on driver's compoters"""

print("Starting ThriftyClient")
import socket
import sys
import os


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

clear()

print("ThriftyClient Started!")

# Set the ip address of the server from the cli
if len(sys.argv) >= 2:
	FMS_ip = str(sys.argv[1])
else:
	FMS_ip = "10.1.0.5"

# Get the team number
print("Enter your team number:")
teamid = str(input(">"))

# Check the team
try:
	teamid = int(teamid)
except:
	print("INVALID TEAM!")
	exit(1)

clear()

# Configuration vars
isConnected = False

# Create socket for sending info to FMS
ds2fms_notify = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ds2fms_notify.connect((FMS_ip, 1742))#1750))

# Send out connection request to driverstation
request = {
	"client_type":"driverstation",
	"team_id":teamid
}
ds2fms_notify.send(str(request).encode())

# Get response from FMS
try:
	response = eval(str(ds2fms_notify.recv(1024).decode()))
except:
	print("Invalid response sent from FMS..")
	input("PRESS ENTER TO CLOSE")
	exit(0)
ds2fms_notify.close()

# Parse data from FMS
assignedStation = response["station"]
isConnected = True
print("Connected to ThriftyField!")

# Wait for user input
print("Press ENTER to enable ThriftyClient")
input("")
clear()

print("-- ThriftyField --")
print("FMS: Connected")

# Check if team should be on field
if assignedStation == None:
	print("Your team is not supposed to be on the field. Please wait until you are called to compete")
	input("PRESS ENTER TO CLOSE")
	exit(0)
else:
	print("Assigned Station: "+ str(assignedStation))

print("Team Number: "+ str(teamid))
print("--- LOG ---")

# Listen on all interfaces for FMS commands
udpconn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpconn.bind((0.0.0.0, 1121))
print("UDP Listener started")

while True:
	try:
		# Recieve data from FMS
		data, addr = udpconn.recvfrom(1024)
	except:
		continue
	
	if not str(add) == str(FMS_ip):
		continue
	
	data = eval(str(data.decode()))
	