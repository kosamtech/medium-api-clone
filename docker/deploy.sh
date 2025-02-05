#!/bin/bash

SHA=$(git rev-parse HEAD)

docker build -t kosamtech/medium-api:latest -t kosamtech/medium-worker:latest -t kosamtech/medium-flower:latest -f ./local/django/Dockerfile ../
docker build -t kosamtech/medium-nginx:latest -f ./local/nginx/Dockerfile ./local/nginx/
docker build -t kosamtech/medium-db:latest -f ./local/postgres/Dockerfile ../ 

docker push kosamtech/medium-api:latest
docker push kosamtech/medium-worker:latest
docker push kosamtech/medium-flower:latest
docker push kosamtech/medium-nginx:latest
docker push kosamtech/medium-db:latest