# Quick Start Guide: AWS Lambda Power Tuning Demo

This guide will help you quickly set up and run the Lambda Power Tuning demo with **x86_64 vs ARM64 architecture comparison**.

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. AWS SAM CLI installed (`pip install aws-sam-cli`)
3. Python 3.11 or later
4. AWS account with permissions to create Lambda functions and Step Functions

## Quick Setup (5 minutes)

### Step 1: Deploy Lambda Functions

**On Windows (PowerShell):**
```powershell
# Deploy both x86_64 and ARM64 versions (recommended for comparison)
.\deploy-all.ps1 -Profile "your-profile" -Region "us-east-1" -ArchitectureType both

# Or deploy only one architecture
.\deploy-all.ps1 -ArchitectureType x86      # x86_64 only
.\deploy-all.ps1 -ArchitectureType arm64    # ARM64 only
```

**On macOS/Linux:**
```bash
chmod +x deploy-all.sh

# Deploy both architectures
./deploy-all.sh your-profile us-east-1 both

# Or deploy only one
./deploy-all.sh your-profile us-east-1 x86
./deploy-all.sh your-profile us-east-1 arm64
```

### Step 2: Deploy Lambda Power Tuning

1. Go to the [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:REGION:ACCOUNT:applications~aws-lambda-power-tuning)
2. Click **Deploy**
3. Accept default settings and deploy the application
4. Note the State Machine ARN from the outputs

### Step 3: Run Power Tuning Analysis

#### Option A: Using AWS Console

1. Open AWS Step Functions console
2. Find the `powerTuningStateMachine`
3. Click **Start execution**
4. Use one of the test payloads from `test-payloads/` directory
5. Replace `REPLACE_WITH_YOUR_FUNCTION_ARN` with your actual function ARN
6. Click **Start execution**

#### Option B: Using AWS CLI

```bash
# Get your function ARN
aws lambda get-function --function-name power-tuning-demo-cpu-intensive --query 'Configuration.FunctionArn'

# Start power tuning execution
aws stepfunctions start-execution \
  --state-machine-arn "YOUR_STATE_MACHINE_ARN" \
  --input file://test-payloads/cpu-intensive-config.json
```

## Understanding the Results

After execution completes, you'll see:

1. **Visualization URL**: Interactive chart showing cost vs performance
2. **Optimal Configuration**: Recommended memory setting based on your strategy
3. **Detailed Metrics**: Execution times and costs for each memory configuration

### Expected Results by Function Type:

| Function Type | Expected Behavior | ARM64 Advantage |
|--------------|-------------------|-----------------|
| **CPU-Intensive** | Significant performance improvement with higher memory (more vCPU) | **20-34% better price/performance** |
| **I/O-Bound** | Minimal improvement with higher memory, optimize for cost | **20% cost savings** |
| **Network-Bound** | **Dramatic jumps at 1769 MB (1 vCPU) & 3537+ MB (2 vCPUs)** | **20-34% better + clear vCPU benefits** |

1. **Run tests on both architectures**:
   - Use `test-payloads/cpu-intensive-x86-config.json` for x86_64
   - Use `test-payloads/cpu-intensive-arm64-config.json` for ARM64

2. **Compare visualization URLs** side-by-side

3. **Key metrics to highlight**:
   - Cost difference (~20% lower for ARM64)
   - Performance difference (varies by workload)
   - Optimal memory configuration for each

4. **Best demo**: CPU-intensive function shows the most dramatic ARM64 benefits

See [test-payloads/ARCHITECTURE-COMPARISON.md](test-payloads/ARCHITECTURE-COMPARISON.md) for detailed comparison guide.

## Testing Each Function

### CPU-Intensive Function
Test with different Fibonacci numbers to see how CPU impacts performance:
```json
{
  "fibonacci": 35,
  "prime_limit": 10000
}
```

### I/O-Bound Function
Test with varying numbers of concurrent requests:
```json
{
  "num_requests": 10
}
```

### Network-Bound Function (Shows 2 vCPU Benefit)
Test with parallel network + CPU processing:
```json
{
  "num_requests": 15,
  "max_workers": 10
}
```
**Key feature**: Use memory values `[512, 1024, 1536, 1769, 2048, 3008, 3537, 4096]` to see performance jumps at vCPU thresholds!

### Memory-Intensive Function
Test with different dataset sizes:
```json
{
  "data_size_mb": 50,
  "threshold": 500
}
```

### Simple API Function
Test basic API response:
```json
{
  "httpMethod": "GET",
  "path": "/health"
}
```

## Power Tuning Strategies

Choose a strategy based on your priorities:

- **cost**: Minimize cost (may be slower)
- **speed**: Minimize execution time (may cost more)
- **balanced**: Balance between cost and speed

## Tips for Demo

1. **Start with network-bound**: Shows the most dramatic vCPU threshold effects
2. **Highlight 1769 MB threshold**: Point out the performance jump at 1 full vCPU
3. **Show 3537+ MB impact**: Demonstrate 2 vCPU power for parallel workloads
4. **Compare architectures**: Run x86_64 vs ARM64 side-by-side
5. **Highlight cost savings**: ARM64 is ~20% cheaper at same memory levels
6. **Use visualization URLs**: Share the interactive charts with your audience
7. **Compare CPU vs I/O**: Show how CPU-intensive benefits more than pure I/O
8. **Run multiple times**: Show consistency in results
3. **Use visualization URLs**: Share the interactive charts with your audience
4. **Run multiple times**: Show consistency in results
5. **Try different payloads**: Demonstrate how workload affects optimal configuration

## Troubleshooting

### Functions not deploying?
- Verify AWS credentials: `aws sts get-caller-identity`
- Check SAM CLI installation: `sam --version`
- Ensure proper IAM permissions

### Power Tuning execution fails?
- Verify function ARN is correct
- Check CloudWatch Logs for function errors
- Ensure payload format is valid JSON

### Timeout errors?
- Increase function timeout in template.yaml
- Reduce workload size in test payload
- Check for external service availability (I/O-bound function)

## Cleanup

When you're done with your demo, clean up all resources to avoid ongoing charges.

### Option 1: Use the Teardown Script (Recommended)

**Windows (PowerShell):**
```powershell
# Delete all Lambda function stacks
.\teardown.ps1 -Profile AWSDeveloper

# Also delete the managed S3 bucket created by SAM
.\teardown.ps1 -Profile AWSDeveloper -DeleteS3Bucket
```

The script will:
- List all stacks that will be deleted
- Ask for confirmation before proceeding
- Delete all 10 Lambda function stacks (5 x86_64 + 5 ARM64)
- Optionally delete the SAM-managed S3 bucket
- Show a summary of the cleanup operation

### Option 2: Manual Deletion via AWS CLI

```bash
# Delete all Lambda function stacks
aws cloudformation delete-stack --stack-name power-tuning-demo-cpu-intensive-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-io-bound-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-network-bound-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-memory-intensive-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-simple-api-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-cpu-intensive-arm64-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-io-bound-arm64-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-network-bound-arm64-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-memory-intensive-arm64-stack --profile AWSDeveloper
aws cloudformation delete-stack --stack-name power-tuning-demo-simple-api-arm64-stack --profile AWSDeveloper

# Delete Power Tuning State Machine (if you deployed it)
aws cloudformation delete-stack --stack-name serverlessrepo-aws-lambda-power-tuning --profile AWSDeveloper
```

### Option 3: AWS Console

1. Go to CloudFormation console
2. Select stacks starting with `power-tuning-demo-`
3. Click **Delete** for each stack
4. Confirm deletion

### Verify Cleanup

Check that all stacks have been deleted:
```bash
aws cloudformation list-stacks --stack-status-filter DELETE_COMPLETE --profile AWSDeveloper --query "StackSummaries[?contains(StackName, 'power-tuning-demo')].StackName"
```

**Note**: Stack deletion is asynchronous and may take a few minutes to complete.

## Additional Resources

- [AWS Lambda Power Tuning Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html)
- [Lambda Power Tuning GitHub](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [AWS Graviton2 Performance](https://aws.amazon.com/ec2/graviton/)
- [Architecture Comparison Guide](test-payloads/ARCHITECTURE-COMPARISON.md)
- [vCPU Threshold Analysis](test-payloads/VCPU-THRESHOLD.md)

## Additional Resources

- [AWS Lambda Power Tuning Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html)
- [Lambda Power Tuning GitHub](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
