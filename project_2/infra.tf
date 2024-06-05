# Define provider
provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

# DynamoDB Table
resource "aws_dynamodb_table" "users_table" {
  name           = "Users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "groups_table" {
  name           = "Groups"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "group_id"

  attribute {
    name = "group_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "messages_table" {
  name           = "Messages"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "message_id"

  attribute {
    name = "message_id"
    type = "S"
  }

  global_secondary_index {
    name               = "receiver_id-index"
    hash_key           = "receiver_id"
    projection_type    = "ALL"
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
        Resource = [
          aws_dynamodb_table.users_table.arn,
          aws_dynamodb_table.groups_table.arn,
          aws_dynamodb_table.messages_table.arn
        ]
      }
    ]
  })
}

# IAM Policy Attachment
resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

# Lambda Functions
# Register User Lambda Function
resource "aws_lambda_function" "register_user_lambda" {
  filename      = "register_user.zip" 
  function_name = "register_user"
  handler       = "register_user.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("register_user.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Block User Lambda Function
resource "aws_lambda_function" "block_user_lambda" {
  filename      = "block_user.zip" 
  function_name = "block_user"
  handler       = "block_user.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("block_user.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Create Group Lambda Function
resource "aws_lambda_function" "create_group_lambda" {
  filename      = "create_group.zip" 
  function_name = "create_group"
  handler       = "create_group.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("create_group.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Add/Remove Users Lambda Function
resource "aws_lambda_function" "add_remove_users_lambda" {
  filename      = "add_remove_users.zip" 
  function_name = "add_remove_users"
  handler       = "add_remove_users.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("add_remove_users.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Send Group Message Lambda Function
resource "aws_lambda_function" "send_group_message_lambda" {
  filename      = "send_group_message.zip" 
  function_name = "send_group_message"
  handler       = "send_group_message.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("send_group_message.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Send Message Lambda Function
resource "aws_lambda_function" "send_message_lambda" {
  filename      = "send_message.zip" 
  function_name = "send_message"
  handler       = "send_message.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("send_message.zip")
  role          = aws_iam_role.lambda_role.arn
}

# Check Messages Lambda Function
resource "aws_lambda_function" "check_messages_lambda" {
  filename      = "check_messages.zip" 
  function_name = "check_messages"
  handler       = "check_messages.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("check_messages.zip")
  role          = aws_iam_role.lambda_role.arn
}

# API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name        = "MyAPI"
  description = "API Gateway for my application"
}

resource "aws_api_gateway_resource" "register_user_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "register_user"
}

# API Gateway Resources
resource "aws_api_gateway_resource" "block_user_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "block_user"
}

resource "aws_api_gateway_resource" "create_group_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "create_group"
}

resource "aws_api_gateway_resource" "add_remove_users_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "add_remove_users"
}

resource "aws_api_gateway_resource" "send_group_message_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "send_group_message"
}

resource "aws_api_gateway_resource" "send_message_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "send_message"
}

resource "aws_api_gateway_resource" "check_messages_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "check_messages"
}

# API Gateway Methods
resource "aws_api_gateway_method" "register_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.register_user_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "block_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.block_user_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "create_group_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.create_group_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "add_remove_users_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.add_remove_users_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "send_group_message_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.send_group_message_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "send_message_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.send_message_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "check_messages_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.check_messages_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# API Gateway Integrations
resource "aws_api_gateway_integration" "register_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.register_user_resource.id
  http_method             = aws_api_gateway_method.register_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.register_user_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "block_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.block_user_resource.id
  http_method             = aws_api_gateway_method.block_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.block_user_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "create_group_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.create_group_resource.id
  http_method             = aws_api_gateway_method.create_group_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.create_group_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "add_remove_users_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.add_remove_users_resource.id
  http_method             = aws_api_gateway_method.add_remove_users_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.add_remove_users_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "send_group_message_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.send_group_message_resource.id
  http_method             = aws_api_gateway_method.send_group_message_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.send_group_message_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "send_message_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.send_message_resource.id
  http_method             = aws_api_gateway_method.send_message_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.send_message_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "check_messages_integration" {
  rest_api_id             = aws_api_gateway_rest_api.my_api.id
  resource_id             = aws_api_gateway_resource.check_messages_resource.id
  http_method             = aws_api_gateway_method.check_messages_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.check_messages_lambda.invoke_arn
}


# API Gateway Deployments
resource "aws_api_gateway_deployment" "my_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  depends_on  = [
    aws_api_gateway_integration.register_user_integration,
    # Add other dependencies as needed
  ]
  stage_name  = "production"
}

# Output API Gateway URL
output "api_gateway_url" {
  value = aws_api_gateway_deployment.my_api_deployment.invoke_url
}