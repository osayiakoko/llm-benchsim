.PHONY: install dev run test docker-build k8-apply k8-delete migrations migrate

install:
	@python -m pip install -r requirements.txt

dev:
	@fastapi dev src/main.py

run:
	@fastapi run src/main.py

test:
	@pytest tests

docker-build:
	@docker build -t benchmark-api-service:latest .

k8-apply:
	@kubectl apply -f k8s/

k8-delete:
	@kubectl delete -f k8s/

migrate:
	@alembic upgrade head

migrations:
	@alembic revision --autogenerate -m "$(msg)"