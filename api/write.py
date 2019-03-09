from api.api import app, jsonify, keys, request
from game.scoring import score

@app.route("/api/write/point", methods=["POST"])
def writePoint():
    if request.form.get("key") in keys:
        global score
        score[0] += int(request.form.get("value"))
        return jsonify({"success": True, "score": score[0]})
    else:
        return jsonify({"success": False, "reason":"invalud key"})

