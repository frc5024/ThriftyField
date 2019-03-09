from api.api import app, jsonify, keys, request
from game.scoring import score

@app.route("/api/keys/request")
def requestKey():
    if "name" in request.args:
        print("A write key is being requested from "+ request.args["name"] +". Enter a key, or press [Enter] to decline.")
        key = input(">")
        if not key:
            return jsonify({"success": False, "reason": "request declined by admin"})
        else:
            keys.append(key)
            return jsonify({"success": True, "key": key})
    else:
        return jsonify({"success":False, "reason":"name argument not found"})

