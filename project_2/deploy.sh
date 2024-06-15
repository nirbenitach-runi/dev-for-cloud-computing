#!/bin/bash

terraform init
AWS_PROFILE="your-aws-profile" terraform apply -auto-approve
