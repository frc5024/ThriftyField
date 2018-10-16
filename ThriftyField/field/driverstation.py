"""Get and Send data to driverstations"""
import socket
import field
import time


TcpListenPort     = 1750
UdpSendPort       = 1121
UdpReceivePort    = 1160
TcpLinkTimeoutSec = 5
UdpLinkTimeoutSec = 1
maxTcpPacketBytes = 4096

stationPositions = {"R1": 0, "R2": 1, "R3": 2, "B1": 3, "B2": 4, "B3": 5}

def FindDriverstations():
	global running
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Listen on all interfaces because we do not have access to FRC's hardware for networking
	s.bind(("0.0.0.0", TcpListenPort))
	s.listen(1)
	
	print("Listening for driverstations on port: "+ str(TcpListenPort))
	# Loop so we don't have to keep spinning up threads
	while True:
		try:
			conn, addr = s.accept()
		except:
			print("Error accepting driverstation connection")
		
		# Get the data
		packet = conn.recv(5)
		if data:
			if not packet[0] == 0 and not packet[1] == 3 and not packet[2] == 24:
				print("Invalid packet")
				comm.close()
				continue
			
			teamid = int(packet[3])<<8 + int(packet[4])
			teamStation = field.getAssignedStation(str(teamid))
			if teamStation == "":
				print("Connection rejected from " + str(addr) + " because they are not supposed to be on the field")
				# Sleep to stop reconnect using all bandwidth
				time.sleep(1)
				conn.close()
			
			print("Found Team: "+ str(teamid))
			
			# Construct response
			status = 0 # Set to 1 if they are in the wrong station. TODO: Implement later
			
			bytes = [0,3,25]
			print("Assigning team "+ str(teamid) +" to station" + str(teamStation))
			bytes.append(stationPositions[teamStation])
			bytes.append(status)
			assignPacket = bytearray(bytes)
			
			conn.write(assignPacket)
			