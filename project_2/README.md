## Exercise #2: Cloud-Based Messaging System

### Overview:
   - The cloud-based messaging provides a set of RESTful APIs for user registration, user blocking, message sending, group creation, user management in groups and checking messages.

## Components:
   - **AWS Lambda**: Serverless compute service to run backend functions.
   - **Amazon API Gateway**: To create, publish, maintain, monitor, and secure the APIs.
   - **Amazon DynamoDB**: NoSQL database service to store user and message data.
   - **Terraform**: Infrastructure as Code tool to manage and provision the infrastructure.

## Instructions:
1. **Building and Running:**
   - Execute `build_and_run.sh` to build the Docker container and start an interactive session.

2. **Deploying Infrastructure:**
   - Inside the Docker session, run `deploy.sh` to initialize Terraform and apply infrastructure changes.
   - Make sure to configure AWS CLI credentials in `~/.aws` directory before deploying.
   - **Important notes:**
        - Ensure AWS CLI credentials are properly configured with the required permissions.
        - Specify your profile in the `deploy.sh` script for deployment.
        - Customize the AWS region in `infra.tf` to match your environment.

3. **Usage:**
   - After deployment, the API Gateway URL will be provided as an output.
   - Use this URL to send requests with required parameters.
   - To test the system using pytest, run:
     ```
     pytest --url=<API_URL>
     ```

## Usage Examples:
- `POST /register_user`
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "password": "test-123" \
            } \
         <API_URL>/register_user
        ```
    - Response example:
        ```
        {
           "user_id": "user-814d" 
        }
        ```

- `POST /send_message` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "sender_id": "user-814d", \
              "password": "test-123", \
              "receiver_id": "user-a35a", \
              "message": "Hello!" \
            } \
         <API_URL>/send_message
        ```

    - Response example:
        ```
        {
           "message": "Message sent to user-a35a." 
        }
        ```

- `POST /check_messages` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "user_id": "user-814d", \
              "password": "test-123", \
            } \
         <API_URL>/check_messages
        ```

    - Response example:
        ```
        {
            "messages": 
                [
                    {
                        "timestamp": "2024-06-15 10:11:48", 
                        "sender_id": "user-a35a", 
                        "message": "Hello!"
                    }
                ]
        }
        ```

- `POST /block_user` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "user_id": "user-814d", \
              "password": "test-123", \
              "blocked_user_id": "user-a35a" \
            } \
         <API_URL>/block_user
        ```

    - Response example:
        ```
        {
           "message": "You have blocked user-a35a." 
        }
        ```

- `POST /create_group` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "members": "user-814d, user-a35a" \
            } \
         <API_URL>/create_group
        ```

    - Response example:
        ```
        {
           "group_id": "group-11az" 
        }
        ```

- `POST /add_remove_users` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "group_id": "group-11az", \
              "user_id": "user-814d", \
              "action": "add" # supports add/remove \
            } \
         <API_URL>/add_remove_users
        ```

    - Response example:
        ```
        {
           "message": "user-814d has been added to the group." 
        }
        ```

- `POST /send_group_message` endpoint:
    - Request example:
        ```
        curl -X POST \
         -H "Content-Type: application/json" \
         -d { \
              "sender_id": "user-814d", \
              "password": "test-123", \
              "group_id": "group-11az", \
              "message": "Hello group!" \
            } \
         <API_URL>/send_group_message
        ```

    - Response example:
        ```
        {
           "message": "Message sent to group-11az." 
        }
        ```

## Scaling Effects Discussion
   - As the system scales from thousands to millions of users, the performance and reliability of AWS Lambda, Amazon API Gateway and Amazon DynamoDB become crucial:  
        - For thousands of users, AWS Lambda handles the load efficiently due to its ability to scale automatically, though occasional cold starts may slightly increase latency. Amazon API Gateway's default limits and caching capabilities are sufficient and DynamoDB's low-latency response times with auto-scaling for read and write capacity units ensure smooth operation. 
        - As user numbers grow to tens of thousands, optimizing Lambda functions to manage concurrency limits and minimize execution time becomes critical. API Gateway requires monitoring and tuning to handle increased traffic, while DynamoDB partitioning and DAX caching improve performance. 
        - At the scale of millions of users, managing Lambda concurrency limits through provisioned concurrency and robust error handling is essential. AWS Global Accelerator and custom domain names with SSL certificates can optimize API Gateway performance globally. DynamoDB's auto-scaling and Global Tables provide low-latency access worldwide, with efficient data modeling ensuring optimal query performance. 

## Author:
Nir Ben Itach, 3rd Year Computer Science & Entrepreneurship Student  
nir.benitach@post.runi.ac.il