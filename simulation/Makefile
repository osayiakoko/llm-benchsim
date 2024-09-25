.PHONY: install run test docker-build k8-apply k8-delete migrate migrations

install:
	@python -m pip install -r requirements.txt

run:
	@python -m src.main 

test:
	@pytest tests

docker-build:
	@docker build -t simulation-service:latest .

k8-apply:
	@kubectl apply -f k8s/

k8-delete:
	@kubectl delete -f k8s/

migrate:
	@alembic upgrade head

migrations:
	@alembic revision --autogenerate -m "$(msg)"
