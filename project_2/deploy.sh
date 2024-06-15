#!/bin/bash

terraform init
AWS_PROFILE="runi" terraform import aws_dynamodb_table.users_table Users
AWS_PROFILE="runi" terraform import aws_dynamodb_table.groups_table Groups
AWS_PROFILE="runi" terraform import aws_dynamodb_table.messages_table Messages
AWS_PROFILE="runi" terraform apply -auto-approve