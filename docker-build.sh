#!/bin/bash

docker build -t fal-ai-playground .
docker run -d -p 3206:3206 \
    --name fal-ai-playground \
    -e FAL_KEY="$FAL_KEY" \
    --restart always \
    fal-ai-playground
