# Makefile for building and pushing homer-resourcespace
VERSION ?= resourcespace
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/resourcespace/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
