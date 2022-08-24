db = {"user": "x", "password": "x!", "host": "x", "port": "3306", "database": "x"}

DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
if __name__ == "__main__":
    from sqlalchemy import create_engine, text

    db = create_engine(DB_URL, encoding="utf-8", max_overflow=0)
    params = {"name": "dog"}
    rows = db.execute(text("SELECT * FROM users WHERE name = :name"), params).fetchall()
    for i in rows:
        print(i["name"])