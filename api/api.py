from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import os
app = Flask(__name__)
try:
    keys = os.environ["THRIFTY_KEYS"].split(":")
    print("Loaded api keys: " + keys)
except:
    print("No api keys found.. Using empty list")
    keys = []

# routes
from api.read import *
from api.keychain import *
from api.write import *

# handelers
@app.errorhandler(404)
def notFound(_):
    return jsonify({"success":False, "reason":"not found"})