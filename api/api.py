from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
app = Flask(__name__)
keys = []

# routes
from api.read import *
from api.keychain import *
from api.write import *

# handelers
@app.errorhandler(404)
def notFound(_):
    return jsonify({"success":False, "reason":"not found"})