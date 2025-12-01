# -----------------------------
# Docker Compose Makefile
# -----------------------------

COMPOSE = docker-compose
SERVICES = backend frontend celery redis postgres

# -----------------------------
# Help
# -----------------------------
help:
	@echo ""
	@echo "Available Make commands:"
	@echo ""
	@echo "  make build          - Build all containers"
	@echo "  make up             - Start all services in detached mode"
	@echo "  make restart        - Restart all running services"
	@echo "  make logs           - View logs (all services) or specific one: make logs s=backend"
	@echo "  make cli s=<svc>    - Open shell inside a service container"
	@echo "  make status         - Show status of all containers"
	@echo ""
	@echo "Examples:"
	@echo "  make logs s=backend"
	@echo "  make cli s=celery"
	@echo ""

# -----------------------------
# Build containers
# -----------------------------
build:
	$(COMPOSE) build

# -----------------------------
# Start services (detached mode)
# -----------------------------
up:
	$(COMPOSE) up -d

# -----------------------------
# Restart all services
# -----------------------------
restart:
	$(COMPOSE) restart

# -----------------------------
# View logs (follow mode)
# Usage: make logs
# Usage: make logs s=backend
# -----------------------------
logs:
	@if [ -z "$(s)" ]; then \
		$(COMPOSE) logs -f; \
	else \
		$(COMPOSE) logs -f $(s); \
	fi

# -----------------------------
# Exec into service container
# Usage: make cli s=backend
# -----------------------------
cli:
	@if [ -z "$(s)" ]; then \
		echo "Usage: make cli s=<service>"; \
	else \
		$(COMPOSE) exec $(s) sh; \
	fi

# -----------------------------
# Status of running containers
# -----------------------------
status:
	$(COMPOSE) ps
