# Makefile for building and pushing github-atlassian
VERSION ?= github-atlassian
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f stacks/github-atlassian/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
