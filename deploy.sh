#!/bin/bash

terraform init
# AWS_PROFILE="runi" terraform import aws_dynamodb_table.parking_lot_table ParkingLotTable
# AWS_PROFILE="runi" terraform import aws_iam_role.lambda_role lambda_execution_role
AWS_PROFILE="runi" terraform apply -auto-approve