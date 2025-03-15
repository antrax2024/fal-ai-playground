#!/bin/bash

docker build -t fal-ai-inpaint .
docker run -d -p 3206:3400 \
    --name fal-ai-playground \
    -e FAL_KEY="$FAL_KEY" \
    --restart always \
    fal-ai-inpaint
