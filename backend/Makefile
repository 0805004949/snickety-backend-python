img = "flask-backend"
app_name = "flask-app"

build:
	docker build -t $(img) .
app:
	docker run -v ~/.aws:/root/.aws -v ~/.ssh:/root/.ssh -it --rm -p 5000:5000 --name $(app_name)  $(img)  python setup.py runserver --host=0.0.0.0 &
run:
	docker run -v $(PWD):/backend -v ~/.aws:/root/.aws  -it --rm -p 5000:5000 --name $(app_name)  $(img) /bin/bash
shell:
	docker exec -it $(app_name)  /bin/bash
pc:
	python setup.py runserver --host=0.0.0.0 &
dev:
	python -m flask run -h 0.0.0.0 -p 5000