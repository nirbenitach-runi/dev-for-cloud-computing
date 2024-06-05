# Define provider
provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

# Define variables
variable "create_entry_lambda" {
  description = "Flag to determine if the entry lambda function should be created"
  type        = bool
  default     = true
}

variable "create_exit_lambda" {
  description = "Flag to determine if the exit lambda function should be created"
  type        = bool
  default     = true
}

# DynamoDB Table
resource "aws_dynamodb_table" "parking_lot_table" {
  name           = "ParkingLotTable"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ticket_id"

  attribute {
    name = "ticket_id"
    type = "S"
  }
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action    = "sts:AssumeRole"
    }]
  })
}

# IAM Policy for DynamoDB access
resource "aws_iam_policy" "dynamodb_policy" {
  name        = "lambda_dynamodb_policy"
  description = "IAM policy for Lambda functions to access DynamoDB"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ],
        Resource = aws_dynamodb_table.parking_lot_table.arn
      }
    ]
  })
}

# IAM Policy Attachment
resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

# Lambda Function - Entry
resource "aws_lambda_function" "entry_lambda" {
  count         = var.create_entry_lambda ? 1 : 0
  filename      = "entry_lambda.zip" 
  function_name = "parking_lot_entry"
  handler       = "entry_lambda.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("entry_lambda.zip")
  role          = aws_iam_role.lambda_role.arn
  
  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.parking_lot_table.name
    }
  }

  # Force the update of existing lambda function
  lifecycle {
    ignore_changes = [
      source_code_hash
    ]
  }
}

# Lambda Function - Exit
resource "aws_lambda_function" "exit_lambda" {
  count         = var.create_exit_lambda ? 1 : 0
  filename      = "exit_lambda.zip" 
  function_name = "parking_lot_exit"
  handler       = "exit_lambda.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("exit_lambda.zip")
  role          = aws_iam_role.lambda_role.arn
  
  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.parking_lot_table.name
    }
  }

  # Force the update of existing lambda function
  lifecycle {
    ignore_changes = [
      source_code_hash
    ]
  }
}

resource "aws_lambda_permission" "parking_lot_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvokeParkingLotEntry"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.entry_lambda[0].function_name  # Assuming count.index = 0 for entry lambda
  principal     = "apigateway.amazonaws.com"

  # Grant permission for all resources within the API Gateway
  source_arn = "${aws_api_gateway_rest_api.parking_lot_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "parking_lot_lambda_permission_exit" {
  statement_id  = "AllowAPIGatewayInvokeParkingLotExit"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.exit_lambda[0].function_name  # Assuming count.index = 0 for exit lambda
  principal     = "apigateway.amazonaws.com"

  # Grant permission for all resources within the API Gateway
  source_arn = "${aws_api_gateway_rest_api.parking_lot_api.execution_arn}/*/*"
}

# API Gateway
resource "aws_api_gateway_rest_api" "parking_lot_api" {
  name = "ParkingLotAPI"
}

resource "aws_api_gateway_resource" "parking_lot_resource" {
  rest_api_id = aws_api_gateway_rest_api.parking_lot_api.id
  parent_id   = aws_api_gateway_rest_api.parking_lot_api.root_resource_id
  path_part   = "entry"
}

resource "aws_api_gateway_resource" "parking_lot_resource_exit" {
  rest_api_id = aws_api_gateway_rest_api.parking_lot_api.id
  parent_id   = aws_api_gateway_rest_api.parking_lot_api.root_resource_id
  path_part   = "exit"
}

resource "aws_api_gateway_method" "parking_lot_method" {
  rest_api_id   = aws_api_gateway_rest_api.parking_lot_api.id
  resource_id   = aws_api_gateway_resource.parking_lot_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "parking_lot_method_exit" {
  rest_api_id   = aws_api_gateway_rest_api.parking_lot_api.id
  resource_id   = aws_api_gateway_resource.parking_lot_resource_exit.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "parking_lot_integration" {
  count                   = var.create_entry_lambda ? 1 : 0
  rest_api_id             = aws_api_gateway_rest_api.parking_lot_api.id
  resource_id             = aws_api_gateway_resource.parking_lot_resource.id
  http_method             = aws_api_gateway_method.parking_lot_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.entry_lambda[count.index].invoke_arn
}

resource "aws_api_gateway_integration" "parking_lot_integration_exit" {
  count                   = var.create_exit_lambda ? 1 : 0
  rest_api_id             = aws_api_gateway_rest_api.parking_lot_api.id
  resource_id             = aws_api_gateway_resource.parking_lot_resource_exit.id
  http_method             = aws_api_gateway_method.parking_lot_method_exit.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.exit_lambda[count.index].invoke_arn
}

resource "aws_api_gateway_deployment" "parking_lot_deployment" {
  rest_api_id = aws_api_gateway_rest_api.parking_lot_api.id
  depends_on  = [
    aws_api_gateway_integration.parking_lot_integration,
    aws_api_gateway_integration.parking_lot_integration_exit,
    aws_lambda_permission.parking_lot_lambda_permission,
    aws_lambda_permission.parking_lot_lambda_permission_exit
  ]
  stage_name  = "production"
}

output "api_gateway_url" {
  value = aws_api_gateway_deployment.parking_lot_deployment.invoke_url
}