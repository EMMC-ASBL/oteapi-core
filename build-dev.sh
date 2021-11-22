#!/bin/sh
docker build --rm --no-cache --pull -f Dockerfile \
       --label "ontotrans.oteapi=development" \
       --target development \
       -t "ontotrans/oteapi-development:latest" .
