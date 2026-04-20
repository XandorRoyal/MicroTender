.PHONY: run
run:
	python -m app

.PHONY: upgrade-db
upgrade-db:
	alembic upgrade head

.PHONY: docker-up
docker-up:
	docker compose up -d

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: docker-logs
docker-logs:
	docker compose logs -f