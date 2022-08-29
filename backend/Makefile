pwd = "/Users/0805004949/personal/snickety-backend-python/backend"
br:
	docker build -t flask-backend .
	docker run -it --rm -p 5000:5000 --name flask-app -v $(pwd):/backend flask-backend  /bin/bash
run:
	docker run -it -p 5000:5000 --rm --name flask-app -v $(pwd):/backend flask-backend python -m flask run -h 0.0.0.0

shell:
	docker exec -it flask-app  /bin/bash
