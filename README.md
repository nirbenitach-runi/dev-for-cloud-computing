## Exercise #1: Parking Lot Management System

### Overview:
This project aims to develop a scalable and efficient parking lot management system using AWS services like Lambda, DynamoDB and API Gateway. The system provides functionalities for vehicle entry and exit tracking, along with calculating parking charges based on parked duration.

## Components:
1. **Terraform Configuration (`parking_lot_infra.tf`):**
   - Defines AWS provider and necessary resources like DynamoDB table, Lambda functions, IAM roles and API Gateway.

2. **Lambda Functions (`entry_lambda.py`, `exit_lambda.py`):**
   - `entry_lambda.py`: Handles vehicle entry by storing entry details (license plate, entry time) into DynamoDB.
   - `exit_lambda.py`: Manages vehicle exit by calculating parking charges based on parked duration and deleting entry record from DynamoDB.

3. **Docker Configuration (`Dockerfile`):**
   - Sets up a Docker container with AWS CLI, Terraform and required dependencies.
   - Provides an isolated environment for Terraform execution.

4. **Deployment Scripts (`build_and_run.sh`, `deploy.sh`):**
   - `build_and_run.sh`: Builds the Docker container and starts an interactive session for Terraform operations.
   - `deploy.sh`: Initializes Terraform and applies infrastructure changes to AWS resources.

5. **Additional Files:**
   - `requirements.txt`: Lists the required Python dependencies.
   - `README.md`: Documentation for the project.

## Instructions:
1. **Building and Running:**
   - Execute `build_and_run.sh` to build the Docker container and start an interactive session.

2. **Deploying Infrastructure:**
   - Inside the Docker session, run `deploy.sh` to initialize Terraform and apply infrastructure changes.
   - Make sure to configure AWS CLI credentials in `~/.aws` directory before deploying.
   - **Important notes:**
        - Ensure AWS CLI credentials are properly configured with the required permissions.
        - Specify your profile in the `deploy.sh` script for deployment.
        - Customize the AWS region in `parking_lot_infra.tf` to match your environment.

3. **Usage:**
   - After deployment, the API Gateway URL will be provided as an output.
   - Use this URL to send POST requests for vehicle entry (`/entry`) and exit (`/exit`) with required parameters.
   - Entry Lambda function stores entry details, while Exit Lambda calculates charges and updates records.

## Author:
Nir Ben Itach, 3rd Year Computer Science & Entrepreneurship Student  
nir.benitach@post.runi.ac.il
