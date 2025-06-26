# Makefile for building and pushing homer-perforce
VERSION ?= perforce
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/perforce/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push