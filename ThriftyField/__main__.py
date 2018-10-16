"""Main file that starts various threads and sets up configs"""

# Library
from threading import Thread

# Local files
from field import field as field

# Create Thread classes
# class DisplayManager(Thread):
# 	def __init__(self):
# 		Thread.__init__(self)

# 	def run(self):
# 		log = logging.getLogger('werkzeug')
# 		log.disabled = True
# 		apiserver.app.logger.disabled = True
# 		apiserver.app.run(port=int(config["field_api_port"]), host= '0.0.0.0')
	
# 	def stop(self):
# 		self.running = False




# Main function
def main():
	print("Starting ThriftyField...")
	field.run()
	# Start the DisplayManager
	# dm = DisplayManager()
	# dm.start()
	
	

if __name__ == "__main__":
	main()