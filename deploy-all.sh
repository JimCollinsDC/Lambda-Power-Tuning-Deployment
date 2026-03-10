#!/bin/bash

# Deploy All Lambda Functions for Power Tuning Demo
# Usage: ./deploy-all.sh [aws-profile] [region] [architecture]
#   architecture: x86, arm64, or both (default: both)

set -e

AWS_PROFILE=${1:-default}
AWS_REGION=${2:-us-east-1}
ARCHITECTURE=${3:-both}

echo "=========================================="
echo "Deploying Lambda Power Tuning Demo Functions"
echo "AWS Profile: $AWS_PROFILE"
echo "AWS Region: $AWS_REGION"
echo "Architecture: $ARCHITECTURE"
echo "=========================================="

# Check for required tools
echo ""
echo "Checking prerequisites..."

# Check for AWS CLI
if ! command -v aws &> /dev/null; then
    echo "ERROR: AWS CLI is not installed or not in PATH"
    echo "Install from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check for SAM CLI
if command -v sam &> /dev/null; then
    SAM_CMD="sam"
    echo "✓ SAM CLI found: $(sam --version)"
elif command -v python &> /dev/null && python -m samcli --version &> /dev/null; then
    SAM_CMD="python -m samcli"
    echo "✓ SAM CLI found (via Python): $(python -m samcli --version)"
else
    echo "ERROR: AWS SAM CLI is not installed or not in PATH"
    echo ""
    echo "Install AWS SAM CLI using one of these methods:"
    echo "  1. Using pip: pip install aws-sam-cli"
    echo "  2. Using Homebrew: brew install aws-sam-cli"
    echo "  3. Download installer: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    echo ""
    echo "After installation, you may need to restart your terminal."
    exit 1
fi

echo "✓ AWS CLI found: $(aws --version)"
echo ""

# Function to deploy a Lambda function
deploy_function() {
    local function_dir=$1
    local function_name=$2
    local template_file=${3:-template.yaml}
    
    echo ""
    echo "Deploying $function_name..."
    cd "$function_dir"
    
    # Create deployment package
    if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt -t ./package
        cp lambda_function.py ./package/
        cd package
        zip -r ../deployment-package.zip .
        cd ..
        rm -rf package
    else
        echo "No dependencies, packaging function only..."
        zip deployment-package.zip lambda_function.py
    fi
    
    # Deploy using SAM
    echo "Deploying with SAM ($template_file)..."
    $SAM_CMD deploy \
        --template-file "$template_file" \
        --stack-name "$function_name-stack" \
        --capabilities CAPABILITY_IAM \
        --region "$AWS_REGION" \
        --profile "$AWS_PROFILE" \
        --no-confirm-changeset \
        --no-fail-on-empty-changeset
    
    # Clean up
    rm -f deployment-package.zip
    
    cd ..
    echo "$function_name deployed successfully!"
}

# Deploy each function based on architecture type
if [ "$ARCHITECTURE" == "x86" ] || [ "$ARCHITECTURE" == "both" ]; then
    echo ""
    echo "=== Deploying x86_64 Functions ==="
    deploy_function "cpu-intensive" "power-tuning-demo-cpu-intensive" "template.yaml"
    deploy_function "io-bound" "power-tuning-demo-io-bound" "template.yaml"
    deploy_function "network-bound" "power-tuning-demo-network-bound" "template.yaml"
    deploy_function "memory-intensive" "power-tuning-demo-memory-intensive" "template.yaml"
    deploy_function "simple-api" "power-tuning-demo-simple-api" "template.yaml"
fi

if [ "$ARCHITECTURE" == "arm64" ] || [ "$ARCHITECTURE" == "both" ]; then
    echo ""
    echo "=== Deploying ARM64 (Graviton2) Functions ==="
    deploy_function "cpu-intensive" "power-tuning-demo-cpu-intensive-arm64" "template-arm64.yaml"
    deploy_function "io-bound" "power-tuning-demo-io-bound-arm64" "template-arm64.yaml"
    deploy_function "network-bound" "power-tuning-demo-network-bound-arm64" "template-arm64.yaml"
    deploy_function "memory-intensive" "power-tuning-demo-memory-intensive-arm64" "template-arm64.yaml"
    deploy_function "simple-api" "power-tuning-demo-simple-api-arm64" "template-arm64.yaml"
fi

echo ""
echo "=========================================="
echo "All functions deployed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Deploy AWS Lambda Power Tuning from AWS Serverless Application Repository"
echo "2. Run power tuning analysis on each function"
echo "3. Compare x86_64 vs ARM64 performance and cost"
echo ""
echo "Function ARNs:"
aws lambda list-functions \
    --profile "$AWS_PROFILE" \
    --region "$AWS_REGION" \
    --query "Functions[?starts_with(FunctionName, 'power-tuning-demo')].{Name:FunctionName,Arch:Architectures[0],Memory:MemorySiz
echo "All functions deployed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Deploy AWS Lambda Power Tuning from AWS Serverless Application Repository"
echo "2. Run power tuning analysis on each function"
echo "3. Compare results to optimize configurations"
echo ""
echo "Function ARNs:"
aws lambda list-functions \
    --profile "$AWS_PROFILE" \
    --region "$AWS_REGION" \
    --query "Functions[?starts_with(FunctionName, 'power-tuning-demo')].{Name:FunctionName,Arn:FunctionArn}" \
    --output table
