# Lambda Power Tuning Test Payloads

This directory contains sample test payloads for each Lambda function to use with AWS Lambda Power Tuning.

## Usage with Lambda Power Tuning

When configuring the Power Tuning State Machine, use these payloads in the `payload` field.

## CPU-Intensive Function

### Light Load
```json
{
  "fibonacci": 30,
  "prime_limit": 5000
}
```

### Medium Load
```json
{
  "fibonacci": 35,
  "prime_limit": 10000
}
```

### Heavy Load
```json
{
  "fibonacci": 38,
  "prime_limit": 20000
}
```

## I/O-Bound Function

### Light Load
```json
{
  "num_requests": 5
}
```

### Medium Load
```json
{
  "num_requests": 10
}
```

### Heavy Load
```json
{
  "num_requests": 20
}
```

## Memory-Intensive Function

### Light Load
```json
{
  "data_size_mb": 25,
  "threshold": 500
}
```

### Medium Load
```json
{
  "data_size_mb": 50,
  "threshold": 500
}
```

### Heavy Load
```json
{
  "data_size_mb": 100,
  "threshold": 500
}
```

## Simple API Function

### Health Check
```json
{
  "httpMethod": "GET",
  "path": "/health"
}
```

### Echo Test
```json
{
  "httpMethod": "POST",
  "path": "/echo",
  "body": "{\"message\": \"test payload\", \"timestamp\": \"2026-02-01T00:00:00Z\"}"
}
```

### Info Request
```json
{
  "httpMethod": "GET",
  "path": "/info"
}
```

## Power Tuning Configuration Example

```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-cpu-intensive",
  "powerValues": [128, 256, 512, 1024, 1536, 2048, 3008],
  "num": 10,
  "payload": {
    "fibonacci": 35,
    "prime_limit": 10000
  },
  "parallelInvocation": true,
  "strategy": "cost"
}
```

### Parameters Explanation:
- **powerValues**: Array of memory values (in MB) to test
- **num**: Number of invocations per memory configuration
- **payload**: Test data for your function
- **parallelInvocation**: Run invocations in parallel (faster testing)
- **strategy**: "cost" (minimize cost) or "speed" (minimize execution time) or "balanced"
