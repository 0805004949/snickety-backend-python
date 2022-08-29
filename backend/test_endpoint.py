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
        {"id": 1, "name": "test11",  "email": "test1@gmail.com","profile": "i love test11", "hashed_password": bcrypt.hashpw("test486!".encode("utf-8"), bcrypt.gensalt())},
        {"id": 2, "name": "test22",  "email": "test2@gmail.com","profile": "i love 222", "hashed_password": bcrypt.hashpw("test486!!".encode("utf-8"), bcrypt.gensalt())},
    ]
    #database.execute(text("insert into users (iㅌd, name, email, profile,hashed_password) values (:id, :name, :email, :profile, :hashed_password)"), new_users[0])
    database.execute(text("insert into users (id, name, email, profile,hashed_password) values (:id, :name, :email, :profile, :hashed_password)"), new_users)  
    database.execute(text("insert into tweets (user_id, tweet) values (2, 'hello world')"))
        


def teardown_function():
    database.execute(text("delete from tweets;"))
    database.execute(text("delete from users_follow_list"))
    database.execute(text("delete  from users"))
    database.execute(text("alter table users auto_increment = 0"))
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



def test_login(api):
    user_info = {"email": "test1@gmail.com", "password": "test486!"}
    resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
    assert b"access_token" in resp.data

def test_anauthorized(api):
    resp = api.post("/follow", data=json.dumps({"follow":2}), content_type="application/json")
    assert resp.status_code == 401

    resp = api.post("/unfollow", data=json.dumps({"unfollow":2}), content_type="application/json")
    assert resp.status_code == 401
    
    contents = {"tweet": "hello world!"}
    resp = api.post("/tweet", data=json.dumps(contents), content_type="application/json")
    assert resp.status_code == 401
    
    
    

def test_follow(api):
    follow_id = 2
    
    # login
    user_info = {"email": "test1@gmail.com", "password": "test486!"}
    resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
    access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]
    
    # user_id =2 tweet does not exists in user_id =1 timeline
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    assert follow_id not in [tweet['user_id'] for tweet in json.loads(resp.data)['timeline']]
    
    # user_id =1 follows user_id = 2
    contents = {"follow":follow_id}
    resp = api.post("/follow", headers={"Authorization": access_token}, data=json.dumps(contents), content_type="application/json")
    assert contents == json.loads(resp.data)
    
    # user_id =2 tweet  exists in user_id=1 timeline
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    assert follow_id in [tweet['user_id'] for tweet in json.loads(resp.data)['timeline']]


def test_unfollow(api):
    unfollow_id = 2
    
    # login
    user_info = {"email": "test1@gmail.com", "password": "test486!"}
    resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
    access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]

    # user_id =2 tweet does not exists in user_id =1 timeline
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    assert unfollow_id not in [tweet['user_id'] for tweet in json.loads(resp.data)['timeline']]
    
    # user_id =1 follows user_id = 2
    contents = {"follow":unfollow_id}
    resp = api.post("/follow", headers={"Authorization": access_token}, data=json.dumps(contents), content_type="application/json")
    assert contents == json.loads(resp.data)
    
    # user_id =2 tweet  exists in user_id=1 timeline
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    assert unfollow_id in [tweet['user_id'] for tweet in json.loads(resp.data)['timeline']]
    
    # user_id =1 unfollows user_id = 2
    contents = {"unfollow":unfollow_id}
    resp = api.post("/unfollow", headers={"Authorization": access_token}, data=json.dumps(contents), content_type="application/json")
    assert contents == json.loads(resp.data)
    
    # user_id =2 tweet does not exists
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    assert unfollow_id not in [tweet['user_id'] for tweet in json.loads(resp.data).get('timeline') if tweet]

def test_tweet(api):
    # login to get token
    user_info = {"email": "test1@gmail.com", "password": "test486!"}
    resp = api.post("/login", data=json.dumps(user_info), content_type="application/json")
    access_token = json.loads(resp.data.decode("UTF-8"))["access_token"]

    # write tweet
    contents = {"tweet": f"im writing bullshits!--{user_info['email']}"}
    resp = api.post("/tweet", headers={"Authorization": access_token}, data=json.dumps(contents), content_type="application/json")
    assert resp.status_code == 200

    # check if i can see my latest tweet
    resp = api.get("/timeline?user_id=1", headers={"Authorization": access_token})
    tweets = json.loads(resp.data)
    assert tweets["timeline"][-1]["tweet"] == contents["tweet"]


