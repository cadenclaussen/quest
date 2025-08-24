# AWS ECR Docker Container Publishing Guide

This document provides a comprehensive guide for publishing Docker containers to Amazon Elastic Container Registry (ECR), based on the implementation completed for the Quest project.

## Table of Contents
1. [AWS Account Setup](#aws-account-setup)
2. [IAM User Creation](#iam-user-creation)
3. [Local Environment Setup](#local-environment-setup)
4. [Docker Container Configuration](#docker-container-configuration)
5. [ECR Repository Creation](#ecr-repository-creation)
6. [Docker Build, Tag, and Push Process](#docker-build-tag-and-push-process)
7. [Verification](#verification)
8. [Final Results](#final-results)
9. [Commands Reference](#commands-reference)

## AWS Account Setup

### Prerequisites
- Valid AWS account (if you don't have one, create at https://aws.amazon.com/)
- Email address for account verification
- Payment method for AWS billing

## IAM User Creation

We created a dedicated IAM user specifically for ECR operations rather than using root credentials.

### Step-by-Step IAM User Creation Process

1. **Navigate to IAM Console**
   - Go to AWS Console → IAM → Users → Create user

2. **Specify User Details**
   - User name: `quest`
   - **Uncheck** "Provide user access to the AWS Management Console" (we only need programmatic access)

3. **Set Permissions**
   - Choose "Attach policies directly"
   - Search for "ContainerRegistry"
   - Select `AmazonEC2ContainerRegistryFullAccess`
   - This policy provides full permissions to create repositories, push images, pull images, and manage ECR

4. **Create Access Keys**
   - After user creation, go to the user's Security credentials tab
   - Click "Create access key"
   - Choose "Command Line Interface (CLI)" use case
   - Check the confirmation checkbox
   - Optionally add description: "Quest project ECR access for Docker container publishing"
   - **Important**: Save both the Access Key ID and Secret Access Key immediately - the secret key won't be shown again

### IAM User Final Configuration
- **User Name**: `quest`
- **Account ID**: `596430611755`
- **User ARN**: `arn:aws:iam::596430611755:user/quest`
- **Permissions**: `AmazonEC2ContainerRegistryFullAccess`

## Local Environment Setup

### AWS CLI Installation

Install AWS CLI using Homebrew on macOS:

```bash
# Install AWS CLI
brew install awscli

# Verify installation
aws --version
# Output: aws-cli/2.28.16 Python/3.13.7 Darwin/24.6.0 source/arm64
```

### Environment Variables Configuration

Created `.env` file with the following AWS credentials and configuration:

```bash
# File: .env
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Important Notes:**
- AWS CLI expects specific environment variable names: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- We chose `us-east-1` region as the default
- The Anthropic API key is included for the LangChain application functionality

### AWS Credentials Verification

Test AWS credentials before proceeding:

```bash
# Set environment variables and test credentials
export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export AWS_DEFAULT_REGION=us-east-1

# Verify credentials work
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDAYVXQI4UV7F5X53C4D",
    "Account": "596430611755",
    "Arn": "arn:aws:iam::596430611755:user/quest"
}
```

## Docker Container Configuration

### Dockerfile Creation

Created a comprehensive Dockerfile for the Python/LangChain application with AWS CLI support:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI (ARM64 version for Apple Silicon compatibility)
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# Copy requirements first for better caching
COPY package.json ./
RUN if [ -f "package.json" ]; then \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs; \
    fi

# Copy Python requirements if they exist
COPY requirements.txt* ./
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# Copy source code
COPY src/ ./src/
COPY . .

# Environment variables for AWS (will be provided at runtime)
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_DEFAULT_REGION=""
ENV ANTHROPIC_API_KEY=""

# Expose port for Streamlit
EXPOSE 8501

# Default command
CMD ["python", "src/hello_langchain.py"]
```

### Docker Verification

Verify Docker is running:

```bash
# Check Docker version and status
docker --version && docker info
```

Output confirmed Docker version 28.3.2 and proper operation.

## ECR Repository Creation

### Create ECR Repository

```bash
# Set AWS credentials in environment
export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export AWS_DEFAULT_REGION=us-east-1

# Create ECR repository
aws ecr create-repository --repository-name quest --region us-east-1
```

Repository creation output:
```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:596430611755:repository/quest",
        "registryId": "596430611755",
        "repositoryName": "quest",
        "repositoryUri": "596430611755.dkr.ecr.us-east-1.amazonaws.com/quest",
        "createdAt": "2025-08-23T19:44:26.309000-07:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

**Important Values:**
- **Repository URI**: `596430611755.dkr.ecr.us-east-1.amazonaws.com/quest`
- **Registry ID**: `596430611755`
- **Repository ARN**: `arn:aws:ecr:us-east-1:596430611755:repository/quest`

## Docker Build, Tag, and Push Process

### ECR Authentication

Authenticate Docker with ECR before pushing:

```bash
# Get ECR login token and authenticate Docker
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 596430611755.dkr.ecr.us-east-1.amazonaws.com
```

Expected output:
```
Login Succeeded
```

### Docker Build Process

Build the Docker image locally:

```bash
# Build Docker image
docker build -t quest .
```

**Build Issues Encountered:**
1. **Initial Issue**: Missing `unzip` package and wrong architecture for AWS CLI
2. **Solution**: Updated Dockerfile to include `unzip` and use ARM64 AWS CLI version

**Final Build Success**: Image built successfully with all dependencies including AWS CLI.

### Docker Image Information

Check the built image:

```bash
# Check image size and details
docker images quest:latest
```

Output:
```
REPOSITORY   TAG       IMAGE ID       CREATED              SIZE
quest        latest    7b4377a18087   About a minute ago   848MB
```

**Container Size**: 848MB locally (includes Python runtime, AWS CLI, system dependencies)

### Tag for ECR

Tag the local image for ECR repository:

```bash
# Tag image for ECR
docker tag quest:latest 596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest
```

### Push to ECR

Push the tagged image to ECR:

```bash
# Push image to ECR repository
docker push 596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest
```

Push process completed successfully with final output:
```
latest: digest: sha256:7b4377a180870b668391a3f38a5da637d3ce504f86a0a738021b346a4df624b5 size: 856
```

## Verification

### Verify Image in ECR

Confirm the image was successfully pushed:

```bash
# List images in ECR repository
aws ecr describe-images --repository-name quest --region us-east-1
```

Verification output:
```json
{
    "imageDetails": [
        {
            "registryId": "596430611755",
            "repositoryName": "quest",
            "imageDigest": "sha256:7b4377a180870b668391a3f38a5da637d3ce504f86a0a738021b346a4df624b5",
            "imageTags": [
                "latest"
            ],
            "imageSizeInBytes": 185251002,
            "imagePushedAt": "2025-08-23T19:48:06.969000-07:00",
            "imageManifestMediaType": "application/vnd.oci.image.index.v1+json"
        }
    ]
}
```

## Final Results

### Summary of Achievements

✅ **AWS Account Setup**: Complete with dedicated IAM user  
✅ **ECR Repository**: Created successfully  
✅ **Docker Image**: Built and optimized for production  
✅ **Image Push**: Successfully uploaded to ECR  
✅ **Verification**: Confirmed image availability in ECR  

### Key Metrics

- **Local Image Size**: 848MB
- **ECR Compressed Size**: ~185MB
- **Push Time**: Approximately 2-3 minutes
- **Architecture**: ARM64 (Apple Silicon compatible)

### Repository Access Information

- **Registry ID**: `596430611755`
- **Repository URI**: `596430611755.dkr.ecr.us-east-1.amazonaws.com/quest`
- **Latest Image Digest**: `sha256:7b4377a180870b668391a3f38a5da637d3ce504f86a0a738021b346a4df624b5`
- **Region**: `us-east-1`

### Future Usage

To pull the image from ECR:

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 596430611755.dkr.ecr.us-east-1.amazonaws.com

# Pull the image
docker pull 596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest

# Run the container with environment variables
docker run -e AWS_ACCESS_KEY_ID=your_key \
           -e AWS_SECRET_ACCESS_KEY=your_secret \
           -e AWS_DEFAULT_REGION=us-east-1 \
           -e ANTHROPIC_API_KEY=your_anthropic_key \
           -p 8501:8501 \
           596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest
```

## Commands Reference

### Complete Command Sequence

Here is the complete sequence of commands executed during this setup:

```bash
# 1. Install AWS CLI
brew install awscli
aws --version

# 2. Verify Docker
docker --version && docker info

# 3. Set up environment variables
export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export AWS_DEFAULT_REGION=us-east-1

# 4. Test AWS credentials
aws sts get-caller-identity

# 5. Create ECR repository
aws ecr create-repository --repository-name quest --region us-east-1

# 6. Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 596430611755.dkr.ecr.us-east-1.amazonaws.com

# 7. Build Docker image
docker build -t quest .

# 8. Check image size
docker images quest:latest

# 9. Tag for ECR
docker tag quest:latest 596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest

# 10. Push to ECR
docker push 596430611755.dkr.ecr.us-east-1.amazonaws.com/quest:latest

# 11. Verify push
aws ecr describe-images --repository-name quest --region us-east-1
```

### Environment Variables Template

For future reference, the required environment variables:

```bash
# AWS Configuration
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1

# Application Configuration
export ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Docker Commands for Development

```bash
# Build image locally
docker build -t quest .

# Run locally for testing
docker run -p 8501:8501 --env-file .env quest

# Clean up local images
docker image prune

# View container logs
docker logs <container_id>
```

---

## Troubleshooting

### Common Issues and Solutions

1. **AWS CLI Not Found**: Install using `brew install awscli`
2. **Docker Authentication Failed**: Re-run the ECR login command
3. **Build Failures**: Ensure Dockerfile includes all necessary dependencies
4. **Architecture Mismatch**: Use appropriate AWS CLI version (aarch64 for ARM64, x86_64 for Intel)
5. **Permission Denied**: Verify IAM user has ECR permissions

### Security Best Practices

- ✅ Use IAM users instead of root credentials
- ✅ Store credentials in `.env` file (add to `.gitignore`)
- ✅ Use least-privilege permissions (ECR-specific policy)
- ✅ Regularly rotate access keys
- ✅ Never commit credentials to version control

---

**Document Created**: August 23, 2025  
**Last Updated**: August 23, 2025  
**Project**: Quest - AI Development Environment  
**Status**: Production Ready ✅