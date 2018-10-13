# Source: https://github.com/Team254/cheesy-arena/blob/master/field/driver_station_connection.go

driverStationTcpListenPort     = 1750
driverStationUdpSendPort       = 1121
driverStationUdpReceivePort    = 1160
driverStationTcpLinkTimeoutSec = 5
driverStationUdpLinkTimeoutSec = 1
maxTcpPacketBytes              = 4096


class DriverStation(object):
	def __init__(self, team: int, station: str, connection):
	self.ip_address = ip
	self.team = team
	self.station = station
	self.con = connection
