from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 0
app.tweets = []

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    msg = payload['tweet']

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(msg) > 300:
        return "300자 초과했습니다", 400
    
    app.tweets.append({"user_id":user_id, "tweet":msg})
    return '',200

    


