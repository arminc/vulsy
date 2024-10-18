# Define the package name
PACKAGE := vulsy

.PHONY: help deps prod-deps validate lint types clean

help:
	@echo "Available targets:"
	@echo "  - make help             		- Show this help message"
	@echo "  - make run 'command'   		- Run the CLI application with the given command"
	@echo "  - make run-with-otel 'command' - Run the CLI application with OpenTelemetry instrumentation and the given command"
	@echo "  - make deps            		- Install all 'dev, test' necessary dependencies for the project"
	@echo "  - make prod-deps       		- Install only the production dependencies"
	@echo "  - make validate        		- Run static code checks, lint and type checking"
	@echo "  - make lint            		- Lint Python files with ruff"
	@echo "  - make types            		- Check type annotations with mypy"
	@echo "  - make clean           		- Remove build artifacts and cache files"
	@echo "  - make test            		- Run unit tests with pytest"
	@echo "  - make test-all            	- Run all tests with pytest"
	@echo "  - make docker up 'all'    		- Start couchbase trough docker compose, use 'all' to also start OpenTelemetry services"
	@echo "  - make docker down 'volumes'	- Stop the docker compose stack, use 'volumes' to also remove volumes"
	@echo "  - make docker up 'test-db'		- Start the test database trough docker compose, it shuts down other docker compose services"
	@echo "  - make docker down 'test-db'		- Stop the test database"
	@echo "  - make docs-serve      		- Serve the documentation locally"
	@echo "Usage: make [TARGET]"

deps:
	pip install -e ".[all]"

prod-deps:
	pip install -e "."

validate: lint types

lint:
	ruff check --select I --fix $(PACKAGE)
	ruff check --select I --fix tests
	ruff format $(PACKAGE)
	ruff check $(PACKAGE)

types:
	mypy $(PACKAGE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache build dist htmlcov

test:
	rm -rf htmlcov
	pytest -m "not database"

test-all:
	rm -rf htmlcov
	pytest

docker:
	@case "$(filter-out docker,$(MAKECMDGOALS))" in \
		"up all") docker compose up -d ;; \
		"up test-db") docker compose down && docker compose -f tests/docker-compose.yaml up -d couchbase ;; \
		"up") docker compose up -d couchbase ;; \
		"down") docker compose down ;; \
		"down test-db") docker compose -f tests/docker-compose.yaml down ;; \
		"down volumes") docker compose down -v ;; \
		*) echo "Usage: make docker [up|up all|up test-db|down|down test-db|down volumes]" ;; \
	esac

run:
	python vulsy/main.py $(filter-out run,$(MAKECMDGOALS))

run-with-otel:
	opentelemetry-instrument python vulsy/main.py $(filter-out run-with-otel,$(MAKECMDGOALS))

docs-serve:
	mkdocs serve
%:
	@: # Do nothing, catch-all target so make doesn't fail on unknown targets
