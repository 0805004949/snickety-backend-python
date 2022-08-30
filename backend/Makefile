pwd = "/home/ec2-user/snickety-backend-python/backend"

b:
	docker build -t flask-backend .
app:
	docker run -it --rm -p 5000:5000 --name flask-app  flask-backend  python setup.py runserver --host=0.0.0.0 &
run:
	docker run -it --rm -p 5000:5000 --name flask-app  flask-backend /bin/bash
shell:
	docker exec -it flask-app  /bin/bash
pc:
	python setup.py runserver --host=0.0.0.0 &