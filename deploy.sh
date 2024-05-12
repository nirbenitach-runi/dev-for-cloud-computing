#!/bin/bash

terraform init
AWS_PROFILE="runi" terraform apply -auto-approve