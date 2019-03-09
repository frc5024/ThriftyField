from api.api import app, jsonify
from game.scoring import score

@app.route("/api/read/score")
def readScore():
    return jsonify({"success": True, "score": score[0]})

