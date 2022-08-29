from flask import Flask, jsonify, request, Response, g, Blueprint, current_app
from sqlalchemy import create_engine, text
import bcrypt
import datetime
import jwt
from flask_cors import CORS
from functools import wraps

bp = Blueprint("app", __name__)


def get_user_info(user_id):
    row = current_app.database.execute(
        text(
            """
                                    select id, name, email, profile from users
                                    where id = :user_id
                                    """
        ),
        {"user_id": user_id},
    ).fetchone()
    if not row:
        return None
    user = {"id": user_id, "email": row["email"], "profile": row["profile"]}

    return user


def login_required(f):
    # 인증절차 이걸 가지고선 토큰이 맞는지 확인
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")

        if access_token is not None:

            try:
                payload = jwt.decode(access_token, current_app.config["JWT_SECRET_KEY"], "HS256")

            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            user_id = payload["user_id"]
            g.user_id = user_id
            g.user = get_user_info(user_id) if user_id else None
        else:  # payload가 비어있지 않다면
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function


def create_app(test_config=None):
    """
    flask가 create_app이라는 이름 함수
    자동으로 팩토리 함수로 인식해 해당함수로 flask 실행
    config인자 받는데 유닛테스트에서 사용하기 편함
    """
    app = Flask(__name__)
    CORS(app)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_pyfile("config.py")
    database = create_engine(app.config["DB_URL"], encoding="utf-8", max_overflow=0)
    app.database = database
    app.config["JWT_SECRET_KEY"] = "김치국마시지마세요!"
    app.register_blueprint(bp)
    return app


# app.id_count = 0
# app.users = {}
# app.tweets = {}

# app = create_app()


@bp.route("/ping", methods=["GET"])
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


@bp.route("/login", methods=["POST"])
def login():
    user = request.json
    pw = user["password"]

    row = current_app.database.execute(text("select id, hashed_password from users where email = :email"), {"email": user["email"]}).fetchone()
    if row and bcrypt.checkpw(pw.encode("utf-8"), row["hashed_password"].encode("utf-8")):  # db에 있는것돠 내가 만든것이 같다면
        payloads = {"user_id": row["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
        token = jwt.encode(payloads, current_app.config["JWT_SECRET_KEY"], "HS256")  # 유효기간 하루
        print(payloads, "<!!!!<")
        return jsonify({"access_token": token})
    else:
        return "fuck you go away", 401


@bp.route("/sign-up", methods=["POST"])
def sign_up():
    """_summary_s
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
    new_user["password"] = bcrypt.hashpw(new_user["password"].encode("utf-8"), bcrypt.gensalt())
    new_user_id = current_app.database.execute(
        text(
            """
                                            insert into users (name, email, profile,hashed_password)
                                            values (:name, :email, :profile, :password)
                                            """
        ),
        new_user,
    ).lastrowid
    row = current_app.database.execute(
        text(
            """
                                    select id, name, email, profile from users
                                    where id = :user_id
                                    """
        ),
        {"user_id": new_user_id},
    ).fetchone()
    created_user = {"id": row["id"], "name": row["name"], "email": row["email"], "profile": row["profile"]} if row else None

    return jsonify(created_user)


@bp.route("/tweet", methods=["POST"])
@login_required
def write_tweet():
    """_summary_
    id, twt 입력
    단, if id not in app.users return not auth(403)

    출력 len(twt)>300 return 400 (bad request)
        len(txt)<300 return request.data
    curl -d '{"id":"1", "tweet":"wtf"}' -H "Content-Type: application/json" -X POST localhost:5000/tweet
    """
    tweet = request.json
    tweet_contents = tweet["tweet"]
    tweet["id"] = g.user_id

    if len(tweet_contents) > 300:
        return "300자를 초과했습니다", 400

    # id검산느안하나?
    current_app.database.execute(
        text(
            """
                              insert into tweets (user_id, tweet)
                              values(:id, :tweet)
                              """
        ),
        tweet,
    )

    return "", 200


@bp.route("/follow", methods=["POST"])
@login_required
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
    payload["id"] = g.user_id

    current_app.database.execute(
        text(
            """
                              insert into users_follow_list (user_id, follow_user_id)
                            values (:id, :follow);
                              """
        ),
        payload,
    )

    return jsonify({"id": g.uer_id, "follow": payload["follow"]}), 200


@bp.route("/unfollow", methods=["POST"])
@login_required
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
    payload["id"] = g.user_id

    current_app.database.execute(
        text(
            """
                              delete from users_follow_list
                              where user_id=:id and follow_user_id=:unfollow
                              """
        ),
        payload,
    )
    return "언팔로우완료", 200


# @bp.route("/timeline/<int:user_id>", methods=["GET"])
# def timeline(user_id):
#     print("fuck")
#     """
#     트위터 타임라인
#     내가 작성했던 트위터와
#     내가 팔로우한느 사람들의 트위터 모드 출력
#     요청 : 사용자 아이디
#     user_tweets = app.tweets[user_id]
#     팔로워리스트 가져오고
#     following = app.users[user_id][follow]
#     그 팔로워들의 트위터들 찾아
#     timeline = []
#     for following in followiing_list:
#         tweets = app.tweets[following]
#         timeline.extend(tweets)
#     리스트형태로 갖다 넣음?
#     출력 : [{},{},{}]
#     """

#     """_summary_
#     curl -d '{"email":"x0805004949@gmail.com", "password":"486", "name":"x0805004949", "profile":"i love this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up
#     curl -d '{"email":"kimchi@gmail.com", "password":"486", "name":"kimchi", "profile":"i hate this book"}' -H "Content-Type: application/json" -X POST http://localhost:5000/sign-up
#     curl -d '{"id":"1", "follow":"2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/follow

#     curl -d '{"id":"1", "tweet":"wtf"}' -H "Content-Type: application/json" -X POST localhost:5000/tweet
#     curl  -X GET localhost:5000/timeline/1

#     :param user_id: _description_
#     :type user_id: _type_
#     :return: _description_
#     :rtype: _type_
#     print(user_id)
#     """
#     r = current_app.database.execute(
#         text(
#             """
#     select t.user_id, t.tweet, t.created_at
#     from tweets t
#     left join users_follow_list as u
#     on u.user_id= :user_id
#     where t.user_id=:user_id or t.user_id=u.follow_user_id;

#                               """
#         ),
#         {"user_id": user_id},
#     ).fetchall()
#     timeline = [{"user_id": row["user_id"], "tweet": row["tweet"]} for row in r]
#     return jsonify({"user_id": user_id, "timeline": timeline})


@bp.route("/timeline", methods=["GET"])
@login_required
def user_timeline():
    # /timeline?user_id=17

    user_id = g.user_id
    if request.args:
        user_id = request.args["user_id"]
    r = current_app.database.execute(
        text(
            """
    select t.user_id, t.tweet, t.created_at
    from tweets t
    left join users_follow_list as u
    on u.user_id= :user_id
    where t.user_id=:user_id or t.user_id=u.follow_user_id;

                              """
        ),
        {"user_id": user_id},
    ).fetchall()
    timeline = [{"user_id": row["user_id"], "tweet": row["tweet"]} for row in r]

    return jsonify({"user_id": user_id, "timeline": timeline})
