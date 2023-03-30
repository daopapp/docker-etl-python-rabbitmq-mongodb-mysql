start:
	docker-compose up -d
stop:
	docker-compose down
enter:
	docker-compose exec app bash
dev:
	docker-compose -f docker-compose-dev.yml up -d
build:
	docker build -t bi-app -f Dockerfile .
