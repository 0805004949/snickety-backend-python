pwd = "/Users/x0805004949/personal/snickety-backend-python/frontend"
br:
	docker build -t flask-frontend-img .
	docker run -it --rm -p 8000:5000 --name frontend-app -v $(pwd):/app flask-frontend-img python -m http.server
run:
	docker run -it -p 8000:5000 --rm --name frontend-app -v $(pwd):/app flask-frontend-img python -m http.server

shell:
	docker exec -it frontend-app /bin/sh
