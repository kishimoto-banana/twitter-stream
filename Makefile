TAG := twitter-stream
DOCKER_CMD := docker

build:
	${DOCKER_CMD} build . -t ${TAG}

run:
	${DOCKER_CMD} run --mount type=bind,source=${PWD}/data,destination=/app/data \
	-it --env-file .env -e TZ=Asia/Tokyo ${TAG}
