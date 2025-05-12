# Makefile for building and pushing homer base image with :base and :latest tags
VERSION ?= base
DOCKER_REPO = mscrnt/homer

build:
	docker build --no-cache \
		-t $(DOCKER_REPO):$(VERSION) \
		-t $(DOCKER_REPO):latest \
		-f homer/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)
	docker push $(DOCKER_REPO):latest

build_and_push: build push
