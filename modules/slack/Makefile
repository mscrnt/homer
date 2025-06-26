# Makefile for building and pushing homer-slack
VERSION ?= slack
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/slack/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push