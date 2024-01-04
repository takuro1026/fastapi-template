VERSION := $(shell /bin/date "+%Y-%m-%d-%H-%M-%S")

SERVICE = hello-app-image

##@ Helpers


.PHONY: help

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) && echo


##@ Release


release: ## build docker image
	@docker build . -f src/Dockerfile \
		--target release \
		-t ${SERVICE}-release


##@ Builds: Service develop docker images


TARGET_TAG := base
# TARGET_TAGS in Dockerfile
TARGET_TAGS := base develop

devs: ## build docker image with targets: ${TARGET_TAGS}
	@for TAG in $(TARGET_TAGS); do \
		echo "Build image with TARGET_TAG: $$TAG"; \
		docker build . -f Dockerfile \
			--target $$TAG -t ${SERVICE}-$$TAG; \
	done


##@ Container Bash


container-bash: ## run docker image with command line: bash with target base
	@echo "Run /bin/bash in container with TARGET_TAG: ${TARGET_TAG}. TARGET_TAG: base develop"
	@docker run \
		-w /opt/dev \
		-v ${PWD}:/opt/dev \
		--rm -it ${SERVICE}-${TARGET_TAG} \
		/bin/bash


##@ Clean


print-built-images: ## print built images
	@docker images | grep ${SERVICE}

clean-built-images: ## clean built images
	@docker images | grep ${SERVICE} | awk '{print $$3}' | xargs docker rmi -f

clean-outputs: ## clean output directory
	@rm -rf outputs


##@ Launches


run-dev: ## run docker-compose with target: develop
	@docker compose -f ./docker-compose-dev.yml up -d --build

down-dev: ## stop docker-compose with target: develop
	@docker compose -f ./docker-compose-dev.yml down

run: ## run release
	@docker compose -f ./docker-compose-prod.yml up -d --build

down: ## stop release
	@docker compose -f ./docker-compose-prod.yml down


##@ TEST
DEVELOP_SERVICE := ${SERVICE}-dev


test: run-dev unit-test down-dev ## run tests

unit-test: ## run unin tests
	@docker-compose -f ./docker-compose-dev.yml exec ${DEVELOP_SERVICE} pytest -vv .


##@ Benchmark


benchmark: run-dev ## run benchmark
	@docker-compose -f ./docker-compose-dev.yml exec ${DEVELOP_SERVICE} \
		locust -f /opt/dev/benchmark/locustfile.py -H http://localhost:8000


##@ Profiling
LIST_SIZE := 10000
TOP_N := 1000
ITERATION := 10
DEVELOP_IMAGE := ${SERVICE}-develop


profiling: ## run profiling
	@docker run \
		-w /opt/dev \
		-v ${PWD}/src/app/core:/opt/dev/core \
		-v ${PWD}/scripts:/opt/dev/scripts \
		--rm -it ${DEVELOP_IMAGE} \
		python3 scripts/profile/profiler.py --list_size ${LIST_SIZE} --top_n ${TOP_N} --iteration ${ITERATION}


##@ Lint


lint: ## py-lint
	@docker run --rm -v ${PWD}:/opt/dev ${DEVELOP_IMAGE} pylint src scripts