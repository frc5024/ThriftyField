import serial
import serial.tools.list_ports
import os
import sys

	
def init():
	print("[FIELD] Starting")
	
	## UNCOMMENT TO ENABLE ARDUINO
	# Find arduino
	# arduinoport = None
	# ports = list(serial.tools.list_ports.comports())
	# for p in ports:
	# 	if "Arduino" in p[1]:
	# 		arduinoport = str(p).split("-")[0][:-1]
	
	# if arduinoport == None:
	# 	print("FCI not found!")
	# 	returndata =  None
	# else:
	# 	try:
	# 		returndata =  serial.Serial(arduinoport, 9600)
	# 	except Exception as e:
	# 		print("Serial error. Type your password below to have it automatically fixed.")
	# 		os.system("sudo chmod 666 " + arduinoport)
	# 	returndata =  serial.Serial(arduinoport, 9600)
	print("[FIELD] Started")
	# return returndata

def getStates(arduino):
	if arduino == None:
		return {"rswitch":["centre", False], "scale":["centre", False], "bswitch":["centre", False]}
	
	data = arduino.read(size=2).decode()
	print(data)
	return {"rswitch":["centre", False], "scale":["centre", False], "bswitch":["centre", False]}

def close(device):
	device.close()