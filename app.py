from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    """_summary_
    curl -d '{"name":"x080", "email":"x080@gmail.com","password":"1234"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up    
    :return: _description_
    :rtype: _type_
    """
    new_user = request.json
    print(jsonify(new_user))
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = +1
    
    return jsonify(new_user) 

@app.route("/tweet", methods=["POST"])
def tweet():
    """_summary_
    curl -d '{"id":"1","tweet":"first-tweet"}' -H "Content-Type: application/json" -X POST http://localhost:5000/tweet
    :return: _description_
    :rtype: _type_
    """
    payload = request.json
    user_id = int(payload['id'])
    msg = payload['tweet']

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(msg) > 300:
        return "300자 초과했습니다", 400
    
    app.tweets.append({"user_id":user_id, "tweet":msg})
    return '',200

    
