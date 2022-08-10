from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.id_count = 0
app.users = {}
app.tweets = {}

db = {
    'user' : '', 
    'password' : '',
    'host' : '', 
    'port' : '3306', 
    'database' :''
}

db_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
db = create_engine(db_url, encoding='utf-8', max_overflow = 0)
params = {'name':'dog'}
rows = db.execute(text("SELECT * FROM users WHERE name = :name"), params).fetchall()
for i in rows:
    print(i['name'])