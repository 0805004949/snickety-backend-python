# python for backend but clean-neat and bit snickety
my journey to follow up python book related to backend.
[here you can buy the book](http://www.yes24.com/Product/Goods/68713424)

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
