## Exercise #1: Parking Lot Management System

### Overview:
   - TEXT

## Components:
   - TEXT
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

## Scaling Effects Discussion
   - TEXT

## Author:
Nir Ben Itach, 3rd Year Computer Science & Entrepreneurship Student  
nir.benitach@post.runi.ac.il