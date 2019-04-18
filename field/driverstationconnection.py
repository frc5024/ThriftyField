import socket
import time

from logging import *

driverstation_tcp_listen_port = 1750
driverstation_udp_send_port = 1121
driverstation_udp_recive_port = 1160
driverstation_tcp_link_timeout_sec = 5
driverstation_dup_link_timeout_sec = 1
max_tcp_packet_bytes = 4096



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
        ip_addr = tcp_conn[1][0]
        notice(f"Driverstation from team {team_id} connected from {ip_addr}")

        self.tcp_conn = tcp_conn
        self.udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_conn.bind((ip_addr, driverstation_udp_recive_port))

        self.team_id = team_id
        self.alliance_station = alliance_station
    

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
        


        
