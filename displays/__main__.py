from flask import Flask
from flask import request
from flask import make_response
import json

app = Flask(__name__)

@app.route('/')
def home():
	# Return a blank page with links to various displays
	# This should be replaced with a proper page at some point
	return '<head><title>ThriftyField - Displays</title></head><body>This is the ThriftyField server. Choose a link:<br><a href="/audiance">Audiance Display</a></body>'

@app.route("/audiance")
def audiance():
	# Open the template file (Read only)
	template = open("./displays/templates/audiance.html", "r").read()
	
	# Return the page
	return template

# Start webserver
if __name__ == '__main__':
	app.run()