# Makefile for building and pushing homer-atlassian
VERSION ?= latest
IMAGE_NAME = homer-atlassian
DOCKER_REPO = mscrnt/$(IMAGE_NAME)

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f modules/atlassian/Dockerfile .

tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_REPO):$(VERSION)

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build tag push
