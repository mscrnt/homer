# Makefile for building and pushing homer-atlassian
VERSION ?= atlassian
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/atlassian/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
