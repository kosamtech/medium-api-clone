build:
	docker compose -f docker-compose-local.yaml up --build -d --remove-orphans

up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down

down-v:
	docker compose -f docker-compose-local.yaml down -v

show-logs:
	docker compose -f docker-compose-local.yaml logs

show-logs-api:
	docker compose -f docker-compose-local.yaml logs api

makemigrations:
	docker compose -f docker-compose-local.yaml run --rm api python manage.py makemigrations

migrate:
	docker compose -f docker-compose-local.yaml run --rm api python manage.py migrate

collectstatic:
	docker compose -f docker-compose-local.yaml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f docker-compose-local.yaml run --rm api python manage.py createsuperuser

volume:
	docker volume inspect medium_local_postgres_data

medium-db:
	docker compose -f docker-compose-local.yaml exec postgres psql --username=kosamtech --dbname=medium-live

flake8:
	docker compose -f docker-compose-local.yaml exec api flake8

black-check:
	docker compose -f docker-compose-local.yaml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f docker-compose-local.yaml exec api black --diff --exclude=migrations .

black:
	docker compose -f docker-compose-local.yaml exec api black --exclude migrations .

isort-check:
	docker compose -f docker-compose-local.yaml exec api isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f docker-compose-local.yaml exec api isort . --diff --skip venv --skip migrations

isort:
	docker compose -f docker-compose-local.yaml exec api isort . --skip venv --skip migrations