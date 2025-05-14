# Makefile for building and pushing homer base image with :base and :latest tags
VERSION ?= base
DOCKER_REPO = mscrnt/homer

build:
	docker build \
		-t $(DOCKER_REPO):$(VERSION) \
		-f homer/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push
