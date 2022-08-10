from flask import Flask, jsonify, request

app = Flask(__name__)
app.id_count = 0
app.users = {}
app.tweets = {}

@app.route("/ping", methods=['GET'])
def ping():
    """_summary_
    endpoint for healthcheck
    curl -X GET 127.0.0.1:5000/ping
    curl -X GET 0.0.0.0:5000/ping
    curl -X GET localhost:5000/ping
    :return: pong
    :rtype: string
    """
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    """_summary_
    회원가입
    app.users = {}
    app.id_count = 1
    
    아이디 카운트에 하나를 더하고
    요청받은 값을 제이슨으로 바꾼다음에
    유저에서 아이디를 키로 나머지 인풋값을 밸류로 하는 딕셔너리에 저장함
    리턴으로는 만든값을 보냄(패스워드제외)
    
    curl -d '{"email":"x0805004949@gmail.com", "password":"486", "name":"x0805004949", "profile":"i love this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    :return: 전체 유저 내용 출력
    :rtype: _type_
    """
    # 함수내에서 request.json을 사용하는 순간 서버는 json 데이터를 받는것을 기대함
    # request.json을 사용하는데 요청에 파라미터가 없다면 400 에러가 뜸
    print(request.json)
    app.id_count+=1
    user_id = app.id_count
    user = request.json
    app.users[user_id] = user
    return jsonify(app.users)

@app.route("/tweet", methods=['POST'])
def write_tweet():
    """_summary_
    id, twt 입력
    단, if id not in app.users return not auth(403)
    
    출력 len(twt)>300 return 400 (bad request)
        len(txt)<300 return request.data
    curl -d '{"id":"1", "tweet":"wtf"}' -H "Content-Type: application/json" -X POST localhost:5000/tweet
    """
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload["tweet"]
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    if len(tweet)>300:
        return "300자를 초과했습니다", 400
    app.tweets.setdefault(user_id, []).append(tweet)

    return app.tweets


"""
"""
@app.route("/follow", methods=['POST'])
def follow():
    """
    팔로잉 구현
    요청 : user_id, following_user_id
    if not user_id, following_user_id  in then return 400 
    user.setdefault(user_id, set()).add(following_user_id)
    curl -d '{"email":"x0805004949@gmail.com", "password":"486", "name":"x0805004949", "profile":"i love this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    curl -d '{"email":"kimchi@gmail.com", "password":"486", "name":"kimchi", "profile":"i hate this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    
    curl -d '{"id":"1", "follow":2}' -H "Content-Type: application/json" -X POST http://localhost:5000/follow 
    """
    payload = request.json
    user_id = int(payload["id"])
    follow_id = int(payload["follow"])
    
    if (user_id not in app.users) or (follow_id not in app.users):
        return "사용자가 존재하지 않습니다", 400
    
    user = app.users[user_id]
    user.setdefault("follow", set()).add(follow_id)
    
    print(app.users)
    return "팔로우완료"


@app.route("/unfollow", methods=['POST'])
def unfollow():
    """
    언팔로잉 구현
    요청 : user_id, following_user_id
    if not user_id, following_user_id  in then return 400 
    user.setdefault(user_id, set()).add(following_user_id)
    curl -d '{"email":"x0805004949@gmail.com", "password":"486", "name":"x0805004949", "profile":"i love this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    curl -d '{"email":"kimchi@gmail.com", "password":"486", "name":"kimchi", "profile":"i hate this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    curl -d '{"id":"1", "follow":"2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/follow
    curl -d '{"id":"1", "unfollow":"2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/unfollow 
    """
    payload = request.json
    user_id = int(payload["id"])
    unfollow_id = int(payload["unfollow"])
    
    if (user_id not in app.users) or (unfollow_id not in app.users):
        return "사용자가 존재하지 않습니다", 400
    
    user = app.users[user_id]
    
    user.setdefault("follow", set()).discard(unfollow_id)
    print(app.users)
    return "언팔로우완료"


@app.route("/timeline/<int:user_id>", methods=['GET'])
def timeline(user_id):
    """
    트위터 타임라인
    내가 작성했던 트위터와 
    내가 팔로우한느 사람들의 트위터 모드 출력
    요청 : 사용자 아이디
    user_tweets = app.tweets[user_id]
    팔로워리스트 가져오고
    following = app.users[user_id][follow]
    그 팔로워들의 트위터들 찾아
    timeline = []
    for following in followiing_list:
        tweets = app.tweets[following]
        timeline.extend(tweets)
    리스트형태로 갖다 넣음?
    출력 : [{},{},{}]
    """


    """_summary_
    curl -d '{"email":"x0805004949@gmail.com", "password":"486", "name":"x0805004949", "profile":"i love this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    curl -d '{"email":"kimchi@gmail.com", "password":"486", "name":"kimchi", "profile":"i hate this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up 
    curl -d '{"id":"1", "follow":"2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/follow

    curl -d '{"id":"1", "tweet":"wtf"}' -H "Content-Type: application/json" -X POST localhost:5000/tweet
    curl  -X GET localhost:5000/timeline/1

    :param user_id: _description_
    :type user_id: _type_
    :return: _description_
    :rtype: _type_
    """
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400   
    
    following = app.users[user_id].get("follow")
    tweets = []
    tweets.append({user_id:app.tweets[user_id]})
    tweets.extend([ {_id:app.tweets[_id]} for _id in following if app.tweets.get(_id) ])
    print(tweets,'<<<<<<<<<<<<<<<')
    
    return "fuxk"