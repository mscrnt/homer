# Makefile for building and pushing perforce-openai
VERSION ?= perforce-openai
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f stacks/perforce-openai/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push