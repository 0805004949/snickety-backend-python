from flask import Flask, request, jsonify

app = Flask(__name__)
app.users = {}
app.id_count = 1

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
    print("dsajkdal")
    print(jsonify(new_user))
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = +1
    
    return jsonify(new_user) 
