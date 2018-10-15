"""Python script to handle starting and stopping the various sections of ThriftyField"""
from threading import Thread

import subprocess

class field(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		self.process = subprocess.Popen(['python3', 'field'])
	
	def stop(self):
		self.process.terminate()

# Create threads
fieldThread = field()

def main():
	# api.start()
	
	print("Type EXIT to stop ThriftyField")
	while True:
		if str(input("")) == "EXIT":
			print("Killing processes")
			fieldThread.stop()

if __name__ == "__main__":
	fieldThread.start()
	main()