pwd = "/Users/0805004949/personal/snickety-backend-python/frontend"
br:
	docker build -t flask-frontend-img .
	docker run -it --rm -p 8000:8000 --name frontend-app -v $(pwd):/frontend flask-frontend-img python -m http.server
run:
	docker run -it -p 8000:8000 --rm --name frontend-app -v $(pwd):/frontend flask-frontend-img python -m http.server

shell:
	docker exec -it frontend-app /bin/sh
