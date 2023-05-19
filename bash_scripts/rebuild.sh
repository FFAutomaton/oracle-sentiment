#!/bin/bash

DOCKER_ID=$(docker ps -aqf "name=oracle-sentiment")
docker stop $DOCKER_ID
docker build --rm -t oracle-sentiment ./
docker run -t -i -d --rm \
    --name nft-mm -v /home/ubuntu/oracle-sentiment/logs:/app/logs \
     nft-mm
