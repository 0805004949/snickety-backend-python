# 깔끔한 파이썬 탄탄한 백엔드 책 리뷰 

# HOW-TO-START
- edit makefile $(pwd) to the abspath where `snickety-backend-python` is  
```
pwd= "blahblabhblavh/snickety-backend-python"
```
- run 
```
$ make br
$ [in-docker-container] FLASK_APP=app.py
$ [in-docker-container] FLASK_DEBUG=1
$ [in-docker-container] cd ./api
$ [in-docker-container] python -m flask run -h 0.0.0.0 -p 5000
```
- why -h option for running flask?
[flask-docs](https://flask.palletsprojects.com/en/1.1.x/quickstart/#what-to-do-if-the-server-does-not-start)
