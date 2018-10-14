from flask import Flask
from flask import request
from flask import make_response
from flask import Response, send_from_directory
import json
# import flask_sse
import requests

# For SSE
from threading import Thread
import time
# from gevent.pywsgi import WSGIServer
import redis

# Create flask app object
app = Flask(__name__)

# Create an sse channel redis db
red = redis.StrictRedis(host='localhost', port=8088, db=0)
def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('gamedata')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']



# Load the master config file
with open("./config.json") as conf:
	config = json.load(conf)

@app.route('/')
def home():
	# Return a blank page with links to various displays
	# This should be replaced with a proper page at some point
	return '<head><title>ThriftyField - Displays</title></head><body>This is the ThriftyField server. Choose a link:<br><a href="/audiance">Audiance Display</a></body>'

@app.route('/subscribe')
def subscribe():
	# The SSE Subscribe URL
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/audiance")
def audiance():
	# Open the template file (Read only)
	template = open("./displays/templates/audiance.html", "r").read()
	
	# Replace placeholder with event name
	template = template.replace("{event.name}", config["event"]["name"])
	template = template.replace("{field.addr}", config["field_api_addr"] + ":" + str(config["field_api_port"]))
	
	
	# Return the page
	return template


# SSE Thread
class SSE(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.running = True

	def run(self):
		i = 0
		while self.running:
			try:
				payload = requests.get(config["field_combined"]+"/api/getall").text
				# red.publish("gamedata", str([payload, i]))
			except:
				print("Could not connect to field")
			payload = requests.get(config["field_combined"]+"/api/getall").text
			# print(payload)
			red.publish("gamedata", payload)
			time.sleep(0.1)
			i += 1
	
	def stop(self):
		self.running = False

# Expose sounds folder
@app.route('/audio/<path:path>')
def send_js(path):
    return send_from_directory('sounds', path)

# Start webserver
if __name__ == '__main__':
	sseloop = SSE()
	sseloop.start()
	app.run(port=int(config["displayserv_port"]), host= '0.0.0.0')
	# server = WSGIServer(("", config["displayserv_port"]), app)
	# server.serve_forever()
	