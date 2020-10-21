#!/usr/bin/make

NAME = "Vane"

CONTAINER_NAME = vane
CONTAINER_TAG = 0.0.1
CONTAINER = $(CONTAINER_NAME):$(CONTAINER_TAG)
PROJECT_DIR = $(shell pwd)
DOCKER_DIR = "/project"

all:
	docker build -t $(CONTAINER) . --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g)
	docker run -t -d --rm --name $(CONTAINER_NAME) -v $(PROJECT_DIR):$(DOCKER_DIR) $(CONTAINER)
	docker exec -it $(CONTAINER_NAME) /bin/bash

.PHONY: clean
clean:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

.PHONY: clean
test:
	pytest --cov-report html --cov=/project/vane/bin tests

.PHONY: exec
exec:
	docker exec -it $(CONTAINER_NAME) /bin/bash
