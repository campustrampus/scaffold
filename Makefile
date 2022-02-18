 export PROJECT_NAME := scaffold
 export SERVICE_NAME := scaffold
 export HELM_SECRETS_VERSION := v3.8.3

# default to local, unless set by ENV
 export DATABASE_URL ?= postgresql://admin:admin@scaffold.localhost:5432/db

.DEFAULT_GOAL := help

.PHONY: help
help: ## View help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: shell
shell: ## Enter the shell for the python virtual environment
	poetry install
	poetry shell

.PHONY: run
run: ## Run the flask app locally. The app will have limited capabilities
	FLASK_APP=entrypoint_app.py FLASK_ENV=development flask run

.PHONY: run-gunicorn
run-gunicorn: ## Run the flask app served by gunicorn locally. The app will have limited capabilities
	gunicorn -w 2 -b:5000 --log-level=info --reload entrypoint_app:app

.PHONY: flask-shell
flask-shell: ## Enter a python shell with context pre-defined for the application
	FLASK_ENV=development flask shell

.PHONY: build
build: ## Build image and run code quality test suite
	docker build -f Dockerfile -t scaffoldi/backend:latest .

.PHONY: format
format: ## Format the codebase using yapf
	yapf -i -r .

.PHONY: lint
lint: ## Lint the codebase using pylint
	pylint --load-plugins pylint_flask_sqlalchemy app tests entrypoint_app.py

.PHONY: tests-unit
tests-unit: ## Run unittests
	FLASK_ENV=testing python -m pytest --cov=app --cov-branch --cov-fail-under=83 --cov-report term-missing -m unittest

.PHONY: tests-int
tests-int: ## Run integration tests
	FLASK_ENV=testing python -m pytest -m integrationtest

.PHONY: asdf-bootstrap
asdf-bootstrap: ## Install all tools through asdf-vm
	@asdf plugin-add helm https://github.com/Antiarchitect/asdf-helm.git > /dev/null || true
	@asdf plugin-add k3d https://github.com/spencergilbert/asdf-k3d.git > /dev/null || true
	@asdf plugin-add kubectl https://github.com/Banno/asdf-kubectl.git > /dev/null || true
	@asdf plugin-add tilt https://github.com/eaceaser/asdf-tilt.git > /dev/null || true
	@asdf plugin-add sops https://github.com/feniix/asdf-sops.git > /dev/null || true
	@asdf install > /dev/null
	helm plugin install https://github.com/jkroepke/helm-secrets --version $(HELM_SECRETS_VERSION) || true

.PHONY: bootstrap
bootstrap: asdf-bootstrap ## Create a k3d K8s cluster for local development
	@PROJECT_NAME=$(PROJECT_NAME) ./k3d-init.sh

.PHONY: up
up: clean bootstrap ## Run a local development environment
	# Default values for testing purposes pulled from the helm chart values for dev
	kubectl config use-context k3d-$(PROJECT_NAME)
	helm dep update deploy/helm/scaffold
	# Use this if a local.secrets.yaml file exists
	# helm secrets upgrade scaffold deploy/helm/scaffold --install -f deploy/helm/local.values.yaml -f deploy/helm/local.secrets.yaml
	helm secrets upgrade scaffold deploy/helm/scaffold --install -f deploy/helm/local.values.yaml
	tilt up --context k3d-$(PROJECT_NAME) --hud
	tilt down

.PHONY: clean
clean: ## Delete local development environment
	@k3d cluster delete $(PROJECT_NAME) || true
	@docker network rm k3d || true
	@rm -rf deploy/helm/scaffold/tmpcharts
	
.PHONY: create-release-branch
create-release-branch: ## Create release branch on main
	git checkout dev
	git pull
	git checkout main
	git pull
	git checkout -b release-`date +%Y-%m-%d`
	echo "run git merge origin/dev. If you have conflicts, resolve them, then git push and create a PR"

.PHONY: helm-template
helm-template: ## Print rendered helm templates
	helm template scaffold deploy/helm/scaffold -f deploy/helm/local.values.yaml --set-file backend.auth0.clientSecret=auth0-secret | sed '$d'

.PHONY: validate-migrations
validate-migrations: ## Fail if migration generation needed
	@export DATABASE_URI="${DATABASE_URL}"; \
	./migrations/migration_manager.sh validate

.PHONY: upgrade-database
upgrade-database: ## apply migration to database
	@export DATABASE_URI="${DATABASE_URL}"; \
	./migrations/migration_manager.sh upgrade

.PHONY: database-history
database-history: ## output history of database migrations
	@export DATABASE_URI="${DATABASE_URL}"; \
	flask db history
	
.PHONY: generate-migration
generate-migration: ## requires arg MESSAGE="message"
	$(if $(MESSAGE),, $(error MESSAGE not set while calling generate-migration))
	./migrations/migration_manager.sh generate "${MESSAGE}"
