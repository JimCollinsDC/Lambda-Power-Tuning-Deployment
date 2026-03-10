# [![Repo](https://img.shields.io/badge/repo-JimCollinsDC/Lambda--Power--Tuning--Deployment-blue)](https://github.com/JimCollinsDC/Lambda-Power-Tuning-Deployment)

# Lambda Power Tuning Deployment
# AWS Lambda Power Tuning Demo

This repository contains sample Lambda functions designed to demonstrate AWS Lambda Power Tuning with both **x86_64** and **ARM64 (Graviton2)** architectures.

## Lambda Functions

Each function is available in both architectures for comparison:

### 1. CPU-Intensive Function (`cpu-intensive/`)
Performs Fibonacci calculations and prime number generation - ideal for demonstrating CPU-bound workloads.
- **x86_64**: `power-tuning-demo-cpu-intensive`
- **ARM64**: `power-tuning-demo-cpu-intensive-arm64`

### 2. I/O-Bound Function (`io-bound/`)
Makes HTTP requests and simulates network I/O - shows how I/O-bound functions benefit from different configurations.
- **x86_64**: `power-tuning-demo-io-bound`
- **ARM64**: `power-tuning-demo-io-bound-arm64`

### 3. Network-Bound Function (`network-bound/`) ⚡ NEW
Combines parallel network I/O with CPU-intensive processing - **demonstrates 2 vCPU threshold benefits at 1769+ MB**.
- **x86_64**: `power-tuning-demo-network-bound`
- **ARM64**: `power-tuning-demo-network-bound-arm64`
- **Key Feature**: Shows performance jump at 1769 MB (1 vCPU) and 3537+ MB (2 vCPUs)

### 4. Memory-Intensive Function (`memory-intensive/`)
Processes large datasets in memory - demonstrates memory allocation impact on performance.
- **x86_64**: `power-tuning-demo-memory-intensive`
- **ARM64**: `power-tuning-demo-memory-intensive-arm64`

### 5. Simple API Function (`simple-api/`)
Basic REST API handler - shows baseline performance characteristics.
- **x86_64**: `power-tuning-demo-simple-api`
- **ARM64**: `power-tuning-demo-simple-api-arm64`

## Deployment

Each function includes:
- Python source code
- `requirements.txt` for dependencies
- CloudFormation template for x86_64 (`template.yaml`)
- CloudFormation template for ARM64 (`template-arm64.yaml`)

### Deploy All Functions

**Windows (PowerShell):**
```powershell
# Deploy both architectures (default)
.\deploy-all.ps1

# Deploy only x86_64
.\deploy-all.ps1 -ArchitectureType x86

# Deploy only ARM64
.\deploy-all.ps1 -ArchitectureType arm64
```

**Linux/macOS:**
```bash
# Deploy both architectures (default)
./deploy-all.sh

# Deploy only x86_64
./deploy-all.sh default us-east-1 x86

# Deploy only ARM64
./deploy-all.sh default us-east-1 arm64
```

## Power Tuning

Use the AWS Lambda Power Tuning tool to analyze each function:
https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:REGION:ACCOUNT:applications~aws-lambda-power-tuning

### Architecture Comparison

Compare x86_64 vs ARM64 performance and cost:
- See [test-payloads/ARCHITECTURE-COMPARISON.md](test-payloads/ARCHITECTURE-COMPARISON.md) for detailed comparison guide
- ARM64 (Graviton2) typically provides **20% lower cost**
- CPU-intensive workloads show **up to 34% better price/performance** on ARM64

### vCPU Allocation Thresholds

Lambda allocates vCPU based on memory:
- **Below 1769 MB**: Fractional vCPU (proportional to memory)
- **1769 MB**: 1 full vCPU
- **3537+ MB**: 2 full vCPUs

See [test-payloads/VCPU-THRESHOLD.md](test-payloads/VCPU-THRESHOLD.md) for detailed analysis with the network-bound function.

### Expected Outcomes by Architecture:

| Function Type | x86_64 Behavior | ARM64 Benefit |
|---------------|-----------------|---------------|
| **CPU-intensive** | Benefits from higher memory/CPU | **20-34% better price/performance** |
| **I/O-bound** | Minimal improvement with memory | **20% cost savings** |
| **Network-bound** | **Major improvement at 1769+ MB (2 vCPU)** | **20-34% better + shows vCPU threshold** |
| **Memory-intensive** | Requires adequate memory | **Better value + performance** |
| **Simple API** | Low baseline, may not need optimization | **20% cost savings** |

### Expected outcomes:
- **CPU-intensive**: Benefits significantly from higher memory/CPU
- **I/O-bound**: Shows minimal improvement with higher memory
- **Network-bound**: Shows dramatic improvement at vCPU thresholds (1769 MB, 3537 MB)
- **Memory-intensive**: Requires adequate memory allocation
- **Simple API**: Low baseline, may not need optimization

## Cleanup

When you're done with your demo, clean up all resources to avoid ongoing charges.

### Using the Teardown Script (Recommended)

```powershell
# Windows PowerShell
.\teardown.ps1 -Profile AWSDeveloper

# Also delete the S3 bucket
.\teardown.ps1 -Profile AWSDeveloper -DeleteS3Bucket
```

The teardown script will:
- Delete all 10 Lambda function stacks (5 x86_64 + 5 ARM64)
- Optionally clean up the SAM-managed S3 bucket
- Show a summary of deleted resources

### Manual Cleanup

Delete all stacks individually:
```bash
aws cloudformation delete-stack --stack-name power-tuning-demo-cpu-intensive-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-io-bound-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-network-bound-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-memory-intensive-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-simple-api-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-cpu-intensive-arm64-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-io-bound-arm64-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-network-bound-arm64-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-memory-intensive-arm64-stack
aws cloudformation delete-stack --stack-name power-tuning-demo-simple-api-arm64-stack
```

## Quick Start

For detailed step-by-step instructions, see [QUICKSTART.md](QUICKSTART.md).

## Additional Resources

- [AWS Lambda Power Tuning Tool](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [AWS Graviton2 Performance](https://aws.amazon.com/ec2/graviton/)
- [Lambda vCPU Allocation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html)
