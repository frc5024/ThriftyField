from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static', static_folder='../static', template_folder='../templates')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

arena = None

def Init(_arena):
    global arena
    arena = _arena

def RunWrapper(port, _):
    app.run(port=port)

@app.route("/")
def index():
    return render_template("index.htm")