# Makefile for building and pushing homer-ghosthub
VERSION ?= latest
IMAGE_NAME = homer-github
DOCKER_REPO = sfddockerhub.corp.blizzard.net/$(IMAGE_NAME)

build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f modules/github/Dockerfile .

tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_REPO):$(VERSION)

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build tag push
