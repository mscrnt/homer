# Flow-ResourceSpace-Slack Stack Makefile

VERSION ?= flow-resourcespace-slack
DOCKER_REPO = mscrnt/homer

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f stacks/flow-resourcespace-slack/Dockerfile .

push:
	docker push $(DOCKER_REPO):$(VERSION)

build_and_push: build push

run:
	docker run -it --rm $(DOCKER_REPO):$(VERSION)

clean:
	docker rmi $(DOCKER_REPO):$(VERSION) || true

.PHONY: build push build_and_push run clean