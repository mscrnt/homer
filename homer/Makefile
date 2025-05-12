# Makefile for building and pushing homer-base
VERSION ?= latest
IMAGE_NAME = homer-base
DOCKER_REPO = mscrnt/$(IMAGE_NAME)

build:
	docker build --no-cache -t $(DOCKER_REPO):$(VERSION) -f homer/Dockerfile .

tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_REPO):$(VERSION)

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build tag push
