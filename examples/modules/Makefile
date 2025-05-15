# EXAMPLE Makefile for building and pushing homer-example
VERSION ?= example
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/<example>/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
