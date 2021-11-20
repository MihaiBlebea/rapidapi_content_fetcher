venv-create:
	python3 -m venv virtualenv

venv-activate:
	. ./virtualenv/bin/activate

venv-lock:
	./virtualenv/bin/pip3 freeze > requirements.txt

venv-install-all:
	./virtualenv/bin/pip3 install -r requirements.txt

venv-install:
	./virtualenv/bin/pip3 install $(package)

docker-api-build:
	docker build -t api:v1.0 .

docker-api-run:
	docker run -v ${PWD}/store:/app/store -d -p 5000:5000 --name api api:v1.0

docker-api: docker-api-build docker-api-run

docker-api-stop:
	docker stop api && docker rm api

ansible-clear_cache:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/clear_cache_do.yaml