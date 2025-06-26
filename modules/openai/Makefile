# Makefile for building and pushing homer-openai
VERSION ?= openai
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/openai/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push