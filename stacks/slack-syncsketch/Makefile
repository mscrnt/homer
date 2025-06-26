# Makefile for building and pushing slack-syncsketch
VERSION ?= slack-syncsketch
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f stacks/slack-syncsketch/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push