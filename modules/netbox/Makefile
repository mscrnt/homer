# Makefile for building and pushing homer-netbox
VERSION ?= netbox
DOCKER_REPO = mscrnt/homer
DOCKERFILE = modules/netbox/Dockerfile

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f $(DOCKERFILE) .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push


 