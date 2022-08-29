from app import create_app
import pytest
from sqlalchemy import create_engine, text
import config
import bcrypt
import json

database = create_engine(config.test_config["DB_URL"])


def setup_function():
    # create a test_user
    new_users = [
        {"id": 1, "email": "test1@gmail.com", "name": "test11", "profile": "i love test11", "pw": bcrypt.hashpw("test486!".encode("utf-8"), bcrypt.gensalt())},
        {"id": 2, "email": "test2@gmail.com", "name": "test22", "profile": "i love test22", "pw": bcrypt.hashpw("test486!!".encode("utf-8"), bcrypt.gensalt())},
    ]
    database.execute(text("insert into users (id, email,name,profile, hashed_password) values (:id,:email,:name ,:profile, :pw"), new_users)
    database.exeucte(text("insert into tweets (user_id, tweet) valeus (2, 'hello world'"))


def teardown_function():
    database.execute(text("delete * from tweets;"))
    database.execute(text("delete * from users_follow_list"))
    database.execute(text("delete * from users"))
    database.execute(text("alter table users auto_increment = 0 "))
    database.execute(text("alter table tweets auto_increment = 0 "))


@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config["TESTING"] = True
    # print(app.config)
    api = app.test_client()
    return api


def test_ping(api):
    resp = api.get("/ping")
    print(resp.data)
    assert b"pong" in resp.data


# # login
# def test_login(api):
#     # twitter test
#     # 트위터를 작성 할려면 로그인을 해야하는데
#     user_info = {"email": "dog-cat@gmail.com", "password": "dog486"}
#     resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")

#     assert b"access_token" in resp.data


# def test_follow(api):
#     # login to get token
#     user_info = {"email": "dog-cat@gmail.com", "password": "dog486"}
#     resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
#     access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]

#     # follow
#     follow_info = {"id": "20", "follow": 13}

#     # see if tweet_list is empty
#     resp = api.get("/timeline?user_id=20", headers={"Authorization": access_token})
#     tweets = json.loads(resp.data)
#     if

#     resp = api.post("/follow", data=json.dumps(follow_info), content_type="application/json", headers={"Authorization": access_token})

#     # 성공했을 경우


# def test_timeline(api):
#     # login to get token
#     user_info = {"email": "dog-cat@gmail.com", "password": "dog486"}
#     resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
#     access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]


# def test_tweet(api):
#     # login to get token
#     user_info = {"email": "dog-cat@gmail.com", "password": "dog486"}
#     resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
#     access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]

#     # write tweet
#     contents = {"tweet": f"im writing bullshits!--{user_info['email']}"}
#     resp = api.post("/tweet", headers={"Authorization": access_token}, data=json.dumps(contents), content_type="application/json")
#     assert resp.status_code == 200

#     # check if i can see my latest tweet
#     resp = api.get("/timeline?user_id=20", headers={"Authorization": access_token})
#     tweets = json.loads(resp.data)
#     assert tweets["timeline"][-1]["tweet"] == contents["tweet"]
