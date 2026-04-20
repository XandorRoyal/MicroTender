.PHONY: run
run:
	python -m app

.PHONY: upgrade-db
upgrade-db:
	alembic upgrade head