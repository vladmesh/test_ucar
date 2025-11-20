.PHONY: dev-start dev-stop start stop makemigration format lint test setup-hooks

dev-start:
	docker compose up --build -d

dev-stop:
	docker compose down

start:
	docker compose -f docker-compose.prod.yml up --build -d

stop:
	docker compose -f docker-compose.prod.yml down

makemigration:
	@if [ -z "$(m)" ]; then echo "Message is required. Usage: make makemigration m='message'"; exit 1; fi
	docker compose run --rm app alembic revision --autogenerate -m "$(m)"
	docker compose run --rm app alembic upgrade head

format:
	docker compose run --rm app ruff format .
	docker compose run --rm app ruff check --fix .

lint:
	docker compose run --rm app ruff check .

test:
	docker compose run --rm app pytest tests/ -v

setup-hooks:
	@echo "Setting up git hooks..."
	@echo "#!/bin/sh\n\necho 'Running pre-commit hook...'\nmake format\ngit add -u" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "#!/bin/sh\n\necho 'Running pre-push hook...'\nmake lint\nmake test" > .git/hooks/pre-push
	@chmod +x .git/hooks/pre-push
	@echo "Git hooks installed successfully!"

