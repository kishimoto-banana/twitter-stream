#!/bin/bash
set -e

dump() {
  echo "dump"
  docker exec -i mongo /usr/bin/mongodump --username root --password example --authenticationDatabase admin -d tweet_db -c tweets --out /dump
  docker cp mongo:/dump ./dump
}

restore() {
  echo "restore"
  docker cp ./dump mongo:/dump
  docker exec -i mongo /usr/bin/mongorestore --username root --password example --authenticationDatabase admin -d tweet_db -c tweets --dir /dump/tweet_db/tweets.bson
}

case "$1" in
  "dump" ) dump ;;
  "restore" ) restore ;;
  * ) exec "$@" ;;
esac
