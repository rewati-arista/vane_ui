#!/usr/bin/make

NAME = "Vane"

CONTAINER_NAME = vane
CONTAINER_TAG = 0.0.1
CONTAINER = $(CONTAINER_NAME):$(CONTAINER_TAG)
PROJECT_DIR = $(shell pwd)
DOCKER_DIR = "/project"
REPO = "registry.gitlab.aristanetworks.com/arista-eosplus/vane"

all:
	docker pull $(REPO)
	docker run -t -d --rm --name $(CONTAINER_NAME) $(REPO)
	docker exec -it $(CONTAINER_NAME) /bin/bash

.PHONY: clean
clean:
	docker stop $(CONTAINER_NAME)

.PHONY: test
test:
	pytest --cov-report html --cov=/project/vane/bin tests
	pytest -vs --cov=/project/vane/bin tests

.PHONY: exec
exec:
	docker exec -it $(CONTAINER_NAME) /bin/bash

.PHONY: format
format:
	docker exec -it $(CONTAINER_NAME) bash -c "black -l 80 /project/vane/bin/*py"

.PHONY: hints
hints:
	docker exec -it $(CONTAINER_NAME) bash -c "mypy /project/vane/bin/*py"

.PHONY: lint
lint:
	docker exec -it $(CONTAINER_NAME) bash -c "pylint /project/vane/bin/*py"

.PHONY: check
check: format lint hints

.PHONY: dev
dev:
	docker build -t $(CONTAINER) . --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g)
	docker run --cap-add=NET_ADMIN --device /dev/net/tun:/dev/net/tun -t -d --rm --name $(CONTAINER_NAME) -v $(PROJECT_DIR):$(DOCKER_DIR) $(CONTAINER)
	docker exec -it $(CONTAINER_NAME) /bin/bash
