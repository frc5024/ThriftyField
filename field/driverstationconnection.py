import socket
import time
import datetime as datetime
from threading import Thread
from game.matchstate import MatchState
import game.matchtiming

from consolelog import *

driverstation_tcp_listen_port = 1750
driverstation_udp_send_port = 1121
driverstation_udp_recive_port = 1160
driverstation_tcp_link_timeout_sec = 5
driverstation_dup_link_timeout_sec = 1
max_tcp_packet_bytes = 4096

alliance_station_position_map = {"R1": 0, "R2": 1, "R3": 2, "B1": 3, "B2": 4, "B3": 5}

class DriverStationConnection:
    team_id = 0
    alliance_station = ""
    auto = False
    enabled = False
    estop = False
    ds_linked = False
    radio_linked = False
    robot_linked = False
    battery_voltage = 0
    ds_robot_trip_time_ms = 0
    missed_packet_count = 0
    seconds_since_last_robot_link = 0
    last_packet_time = 0
    last_robot_linked_time = 0
    packet_count = 0
    missed_packet_offset = 0
    tcp_conn = (None, None)
    udp_conn = (None, None)

    def __init__(self, team_id: int, alliance_station: str, tcp_conn: tuple):
        self.ip_addr = tcp_conn[1][0]
        notice(f"Driverstation from team {team_id} connected from {ip_addr}")

        self.tcp_conn = tcp_conn
        self.udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_conn.bind((ip_addr, driverstation_udp_recive_port))

        self.team_id = team_id
        self.alliance_station = alliance_station
    
    
    
def EncodeControlPacket(arena, dsconn: DriverStationConnection):
    packet = [0 for i in range(22)]

    # Packet number
    packet[0] = (dsconn.packet_count >> 8) & 0xff
    packet[1] = dsconn.packet_count & 0xff

    # Protocol version
    packet[2] = 0

    # Robot status
    packet[3] = 0
    if dsconn.auto:
        packet[3] |= 0x02
    if dsconn.enabled:
        packet[3] |= 0x04
    if dsconn.estop:
        packet[3] |= 0x80
    
    # Unknown
    packet[4] = 0

    # Alliance station
    packet[5] = alliance_station_position_map[dsconn.alliance_station]

    # Match type
    # TODO: un-hard code this value
    # Curently only sends practice
    packet[6] = 1

    # Match number
    # TODO: un-hard code this value
    # Currently only sends 1
    match_number = 1
    packet[7] = match_number >> 8
    packet[8] = match_number & 0xff

    # Replay number
    packet[9] = 1

    # Date and time
    packet[10] = ((time.time_ns() / 1000) >> 24) & 0xff
    packet[11] = ((time.time_ns() / 1000) >> 16) & 0xff
    packet[12] = ((time.time_ns() / 1000) >> 8) & 0xff
    packet[13] = (time.time_ns() / 1000) & 0xff
    packet[14] = time.time() % 60
    packet[15] = time.time() / 60
    packet[16] = packet[15] / 60
    year, month, day = (int(i) for i in str(datetime.datetime.now()).split(" ")[0].split("-"))
    packet[17] = day
    packet[18] = month
    packet[19] = year - 1900

    # Seconds remaining in the current period
    match_seconds_remaining = 0
    if arena.match_state == MatchState.auto_period:
        match_seconds_remaining = game.matchtiming.auto_duration_sec - arena.MatchTimeSec()
    elif arena.match_state == MatchState.teleop_period:
        match_seconds_remaining = game.matchtiming.auto_duration_sec + game.matchtiming.teleop_duration_sec - arena.MatchTimeSec()

    packet[20] = match_seconds_remaining >> 8 & 0xff
    packet[21] = match_seconds_remaining & 0xff

    # Increment packet counter
    dsconn.packet_count += 1

    return bytes(packet)

def SendControlPacket(arena, dsconn):
    packet = EncodeControlPacket(arena, dsconn)
    if dsconn.udp_conn != None:
        dsconn.udp_conn.sendto(packet,(dsconn.ip_addr, driverstation_udp_send_port))

def ListenForDsUdpPackets(arena, _):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", driverstation_udp_recive_port))
    while True:
        data, addr = sock.recvfrom(50)

        team_id = int(data[4]) << 8 + int(data[5])

        ds_conn = None
        for alliance_station in arena.alliance_stations:
            if alliance_station.team != None and alliance_station.team.id == team_id:
                ds_conn = alliance_station.driverstation_connection
                break
        
        if ds_conn != None:
            ds_conn.ds_linked = True
            ds_conn.last_packet_time = time.time()

            ds_conn.radio_linked = data[3] & 0x10 != 0
            ds_conn.robot_linked = data[3] & 0x20 != 0
            
            if ds_conn.robot_linked:
                ds_conn.last_robot_linked_time = time.time()

                # Battery voltage. Stored as volts * 256
                ds_conn.battery_voltage = float(data[6]) + float(data[7]) / 256

def ListenForDriverstations(arena, _):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("10.0.100.5", driverstation_tcp_listen_port))
    except:
        warn("Driverstations expect to find the field on 10.0.100.5 but that is not the address of this computer")
        notice("ThriftyField switched to development mode and has rebound to 0.0.0.0")
        notice("ThriftyField is now listening on all interfaces")
        s.bind(("0.0.0.0", driverstation_tcp_listen_port))
    
    notice(f"Listening for Driverstations on TCP port {driverstation_tcp_listen_port}")
    s.listen(1)

    while True:
        conn, addr = s.accept()
        notice(f"Accepting connection from {addr[0]}")

        data = conn.recv(5)
        if not data:
            error(f"Invalid initial packet")
            conn.close()
            continue
        
        if not (data[0] == 0 and data[1] == 3 and data[2] == 24):
            error(f"Invalid packet: {data}")
            conn.close()
            continue
        
        team_id = int(data[3]) << 8 + int(data[4])

        assigned_station = arena.GetAssignedAllianceStation(team_id)

        if assigned_station == "":
            notice(f"Rejecting connection from team {team_id}, who is not supposed to be on the field")
            time.sleep(1)
            conn.close()
            continue
        
        station_status = bytes(0)

        team_string = str(addr[1]).split(".")
        
        team_digit_1 = int(team_string[1])
        team_digit_2 = int(team_string[2])

        station_team_id = team_digit_1 * 100 + team_digit_2
        if station_team_id != team_id:
            wrong_assigned_station = arena.GetAssignedAllianceStation(station_team_id)
            if wrong_assigned_station != "":
                notice(f"Team {team_id} is in incorrect station {wrong_assigned_station}")
                station_status = 1
        
        assignment_packet = [0, 3, 25, 0, 0]
        notice(f"Accepting connection form Team {team_id} in station {assigned_station}")
        assignment_packet[3] = alliance_station_position_map[assigned_station]
        assignment_packet[4] = station_status

        conn.send(bytes(assignment_packet))
        
        dsconn = DriverStationConnection(team_id, assigned_station, (conn, addr))

        arena.alliance_stations[assigned_station].driverstation_connection = dsconn

        arena.alliance_stations[assigned_station].tcp_conn_thread = Thread(target=HandleTcpConnection, args=(arena, arena.alliance_stations[assigned_station].driverstation_connection))
        arena.alliance_stations[assigned_station].tcp_conn_thread.start()

def HandleTcpConnection(arena, dsconn):
    while True:
        data = dsconn.tcp_conn.recv(max_tcp_packet_bytes)
        if not data:
            error(f"Error reading from connection for team {dsconn.team_id}")
            dsconn.tcp_conn.close()
            arena.alliance_stations[assigned_station].driverstation_connection = None
            break
        
        packet_type = int(data[2])

        if packet_type == 22:
            # Robot status
            status_packet = data[2:38]
            DecodeStatusPacket(dsconn, status_packet)

def DecodeStatusPacket(dsconn, packet):
    dsconn.ds_robot_trip_time_ms = int(data[1]) / 2
    dsconn.missed_packet_count = int(data[2]) - dsconn.missed_packet_offset


        
