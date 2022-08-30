pwd = "/Users/0805004949/ws/snickety-backend-python/backend"
br:
	docker build -t flask-backend .
	docker run -it --rm -p 5000:5000 --name flask-app -v $(pwd):/backend -v ~/.aws:/root/.aws flask-backend python -m flask run -h 0.0.0.0
app:
	docker run -it --rm -p 5000:5000 --name flask-app -v $(pwd):/backend -v ~/.aws:/root/.aws flask-backend python -m flask run -h 0.0.0.0

run:
	docker run -it --rm -p 5000:5000 --name flask-app -v $(pwd):/backend -v ~/.aws:/root/.aws flask-backend /bin/bash

shell:
	docker exec -it flask-app  /bin/bash
