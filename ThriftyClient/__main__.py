"""Client program to be run on driver's compoters"""

print("Starting ThriftyClient")
import socket
import sys
import os
import pyautogui
from threading import Thread


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

# Put all of the actual ds code on its own thread for easy shutdown
class DS(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		# Listen on all interfaces for FMS commands
		udpconn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udpconn.bind(("0.0.0.0", 1121))
		print("UDP Listener started")
		
		while True:
			try:
				# Recieve data from FMS
				data, addr = udpconn.recvfrom(1024)
			except:
				continue
			
			
			# Pares data from FMS
			data = eval(str(data.decode()))
			
			source = data["source"]
			state = data["robot_state"]
			keepConnection = data["stay_connected"]
			
			# Close program if instructed to
			if not keepConnection:
				print("Disconnected from "+ str(source))
				exit(0)
			
			if state == "enable":
				print("Enabling Robot")
				# Inject keystrokes into driverstation
				pyautogui.keyDown("[")
				pyautogui.keyDown("]")
				pyautogui.keyDown("\\")
				
				pyautogui.keyUp("[")
				pyautogui.keyUp("]")
				pyautogui.keyUp("\\")
				print("Signal sent")
			
			elif state == "disable":
				print("Disabling Robot")
				pyautogui.press("enter")
				print("Signal sent")
			
			elif state == "estop":
				print("ESTOP SENT FROM FMS!!!")
				pyautogui.press("space")
				print("Signal sent")

# Start the program
dsthread = DS()
dsthread.start()

print("Type EXIT to stop")
while True:
	if input("") == "EXIT":
		print("Press CTRL+C")
		exit(0)