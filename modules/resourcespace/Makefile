# Makefile for building and pushing homer-resourcespace
VERSION ?= latest
IMAGE_NAME = homer-resourcespace
DOCKER_REPO = mscrnt/$(IMAGE_NAME)

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/resourcespace/Dockerfile .

tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_REPO):$(VERSION)

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build tag push
