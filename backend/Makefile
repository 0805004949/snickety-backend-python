pwd = "/home/ec2-user/snickety-backend-python/backend"

br:
	docker build -t flask-backend .
	docker run -it --rm -p 5000:5000 --name flask-app  flask-backend python setup.py runserver --host=0.0.0.0 &
app:
	docker run -it --rm -p 5000:5000 --name flask-app  flask-backend  python setup.py runserver --host=0.0.0.0 &
run:
	docker run -it --rm -p 5000:5000 --name flask-app  flask-backend flask-backend /bin/bash
shell:
	docker exec -it flask-app  /bin/bash
