# Makefile for building and pushing homer-github
VERSION ?= github
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/github/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
