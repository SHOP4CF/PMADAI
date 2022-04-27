SHELL := /bin/bash

define test_module
    echo "Testing $(1)..." && \
	source $(1)/venv/bin/activate && pytest $(1) && deactivate
endef

dev-down:
	docker-compose -f docker-compose.dev.yml --env-file .env.dev down

dev-build:
	docker-compose -f docker-compose.dev.yml --env-file .env.dev build

dev-up:
	docker-compose -f docker-compose.dev.yml --env-file .env.dev up

prod-down:
	docker-compose -f docker-compose.prod.yml --env-file .env.prod down

prod-build:
	docker-compose -f docker-compose.prod.yml --env-file .env.prod build

prod-up:
	docker-compose -f docker-compose.prod.yml --env-file .env.prod up

test:
	$(call test_module, preprocessing)