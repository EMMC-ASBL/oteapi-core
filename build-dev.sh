#!/bin/sh
docker build --rm -f Dockerfile \
       --label "ontotrans.oteapi=development" \
       --target development \
       -t "ontotrans/oteapi-development:latest" .
