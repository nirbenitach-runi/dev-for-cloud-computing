#!/bin/bash

docker build -t terraform-container .
docker run -it --rm --name terraform -v ~/.aws:/root/.aws terraform-container