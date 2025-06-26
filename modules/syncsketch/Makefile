# Makefile for building and pushing homer-syncsketch
VERSION ?= syncsketch
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/syncsketch/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push