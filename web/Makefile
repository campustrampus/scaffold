
.DEFAULT_GOAL := help

.PHONY: help
help: ## View help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build 
build: .scaffold-ui-build-flag ## Build the container

.scaffold-ui-build-flag:
	docker build -t scaffold-ui-local:latest --target local .
	docker build -t scaffold-ui-optimized:latest --target optimized .
	touch .scaffold-ui-build-flag


.PHONY: run-local
run-local: .scaffold-ui-build-flag ## run the ui container locally
	docker run --rm -it -p 3000:3000 scaffold-ui-local:latest

.PHONY: run-optimized
run-optimized: .scaffold-ui-build-flag ## run the ui container locally
	docker run --rm -it -p 3000:3000 scaffold-ui-optimized:latest

.PHONY: clean
clean: ## clean up to start over
	-rm .scaffold-ui-build-flag
	-docker image rm scaffold-ui-local:latest
	-docker image rm scaffold-ui-optimized:latest
	-rm -r build/*

.PHONY: deepclean
deepclean: clean ## remove docker cache images as well as run clean target
	-docker rmi $$(docker images -f "dangling=true" -q)

