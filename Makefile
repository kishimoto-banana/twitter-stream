TAG := twitter-stream
DOCKER_CMD := docker-compose

build:
	${DOCKER_CMD} build

run:
	${DOCKER_CMD} up -d

stop:
	${DOCKER_CMD} stop

logs-app:
	${DOCKER_CMD} logs -f app

dump:
	./mongo.sh dump

restore:
	./mongo.sh restore