from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

def create_app(test_config=None): 
    """
    flask가 create_app이라는 이름 함수
    자동으로 팩토리 함수로 인식해 해당함수로 flask 실행
    config인자 받는데 유닛테스트에서 사용하기 편함
    """
    app = Flask(__name__)
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_pyfile("config.py")
    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database
    return app
    
# app.id_count = 0
# app.users = {}
# app.tweets = {}

app = create_app()
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
    new_user = request.json
    new_user_id = app.database.execute(text("""
                                            insert into users (name, email, profile,hashed_password)
                                            values (:name, :email, :profile, :password)
                                            """), new_user).lastrowid
    row = app.database.execute(text("""
                                    select id, name, email, profile from users
                                    where id = :user_id
                                    """), {'user_id':new_user_id}).fetchone()
    created_user = {
        'id' : row['id'],
        'name' : row['name'],
        'email' : row['email'],
        'profile' : row['profile']
    } if row else None
    
    return jsonify(created_user)

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