""" Communicate with the ThriftyClient """
import socket
from field import field as field

TcpListenPort     = 1742#1750
UdpSendPort       = 1121
UdpReceivePort    = 1160
TcpLinkTimeoutSec = 5
UdpLinkTimeoutSec = 1
maxTcpPacketBytes = 4096

DriverStationConnection = {
	"TeamId"                    : 0,
	"AllianceStation"           : "",
	"Auto"                      : False,
	"Enabled"                   : False,
	"Estop"                     : False,
	"DsLinked"                  : False,
	"MissedPacketCount"         : 0,
	"lastPacketTime"            : 0,
	"packetCount"               : 0,
	"missedPacketOffset"        : 0,
	"tcpConn"                   : None,
	"udpConn"                   : None
}


def createDSconn(teamid, allianceStation, tcpConnection, addr):
	# Get just the ip address
	ipadress, _ = addr
	
	print("Driver station for Team "+ str(teamid) +" connected from "+ str(ipadress))
	
	udpConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
	# Create a new dict to be returned
	output = DriverStationConnection
	output["TeamId"] = teamid
	output["AllianceStation"] = allianceStation
	output["tcpConn"] = tcpConnection
	output["udpConn"] = [udpConnection, ipadress, UdpSendPort]
	
	return output
	

def listenForDS():
	"""Listen for driverstations and handle them"""
	# Create and bind to TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", TcpListenPort))
	s.listen(1)
	
	while True:
		conn, addr = s.accept()
		try:
			data = str(conn.recv(1024).decode())
		except:
			print("Error decoding data sent by "+ str(addr))
			conn.close()
			continue
		
		# Parse data sent
		data = eval(data)
		teamid = data["team_id"]
		clienttype = data["client_type"]
		
		print("Found "+ str(clienttype) + " at: "+ str(addr))
		
		# Construct a response
		response = {}
		response["station"] = field.getAssignedStation(str(teamid))
		print("Sending assignment data to: "+ str(addr))
		conn.send(str(response).encode())
		conn.close()
		dsconn = createDSconn(teamid, response["station"], conn, addr)
		field.allianceStations[response["station"]]["DsConnection"] = dsconn

# DS commands
def enable(udpconn):
	message = {
		"source": "FMS",
		"robot_state": "enable",
		"stay_connected": True
	}
	udpconn[0].sendto(str(message).encode(), (udpconn[1], udpconn[2]))

def disable(udpconn):
	message = {
		"source": "FMS",
		"robot_state": "disable",
		"stay_connected": True
	}
	udpconn[0].sendto(str(message).encode(), (udpconn[1], udpconn[2]))

def estop(udpconn):
	message = {
		"source": "FMS",
		"robot_state": "estop",
		"stay_connected": True
	}
	udpconn[0].sendto(str(message).encode(), (udpconn[1], udpconn[2]))

def disconnect(udpconn):
	message = {
		"source": "FMS",
		"robot_state": "disable",
		"stay_connected": False
	}
	udpconn[0].sendto(str(message).encode(), (udpconn[1], udpconn[2]))