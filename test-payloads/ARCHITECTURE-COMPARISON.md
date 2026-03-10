# x86_64 vs ARM64 (Graviton2) Comparison Configurations

These configurations are designed to compare the performance and cost of x86_64 vs ARM64 architectures.

## How to Use

1. Run power tuning on the x86_64 version of a function
2. Run power tuning on the ARM64 version of the same function
3. Compare the results side-by-side
4. Note the cost savings and performance differences

## Expected Results

According to AWS, ARM64 (Graviton2) typically provides:
- **20% lower cost** at the same memory configuration
- **Up to 34% better price/performance** for compute-intensive workloads
- **Similar or better performance** for most workloads

## CPU-Intensive Comparison

### x86_64 Configuration
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
  "strategy": "balanced"
}
```

### ARM64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-cpu-intensive-arm64",
  "powerValues": [128, 256, 512, 1024, 1536, 2048, 3008],
  "num": 10,
  "payload": {
    "fibonacci": 35,
    "prime_limit": 10000
  },
  "parallelInvocation": true,
  "strategy": "balanced"
}
```

**What to look for:**
- ARM64 should show better performance at the same memory levels
- Cost should be ~20% lower for ARM64
- CPU-intensive tasks benefit most from Graviton2

## I/O-Bound Comparison

### x86_64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-io-bound",
  "powerValues": [128, 256, 512, 1024, 1536, 2048],
  "num": 10,
  "payload": {
    "num_requests": 10
  },
  "parallelInvocation": true,
  "strategy": "cost"
}
```

### ARM64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-io-bound-arm64",
  "powerValues": [128, 256, 512, 1024, 1536, 2048],
  "num": 10,
  "payload": {
    "num_requests": 10
  },
  "parallelInvocation": true,
  "strategy": "cost"
}
```

**What to look for:**
- Performance differences may be minimal (I/O-bound)
- ARM64 still provides 20% cost savings
- Both architectures should show similar execution patterns

## Memory-Intensive Comparison

### x86_64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-memory-intensive",
  "powerValues": [512, 1024, 1536, 2048, 3008],
  "num": 10,
  "payload": {
    "data_size_mb": 50,
    "threshold": 500
  },
  "parallelInvocation": true,
  "strategy": "balanced"
}
```

### ARM64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-memory-intensive-arm64",
  "powerValues": [512, 1024, 1536, 2048, 3008],
  "num": 10,
  "payload": {
    "data_size_mb": 50,
    "threshold": 500
  },
  "parallelInvocation": true,
  "strategy": "balanced"
}
```

**What to look for:**
- ARM64 memory operations are often faster
- Cost savings consistent across memory levels
- Better value for data processing workloads

## Simple API Comparison

### x86_64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-simple-api",
  "powerValues": [128, 256, 512, 1024],
  "num": 10,
  "payload": {
    "httpMethod": "GET",
    "path": "/health"
  },
  "parallelInvocation": true,
  "strategy": "cost"
}
```

### ARM64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-simple-api-arm64",
  "powerValues": [128, 256, 512, 1024],
  "num": 10,
  "payload": {
    "httpMethod": "GET",
    "path": "/health"
  },
  "parallelInvocation": true,
  "strategy": "cost"
}
```

**What to look for:**
- Minimal execution time differences
- ARM64 provides consistent 20% cost savings
- Optimal for cost optimization with simple workloads

## Analysis Tips

### Creating Comparison Charts

After running both versions:

1. **Export Results**: Save the visualization URLs from both runs
2. **Compare Metrics**:
   - Execution time at same memory level
   - Cost at same memory level
   - Optimal configuration for each architecture
   - Total cost savings with ARM64

3. **Calculate Savings**:
   ```
   Cost Savings % = ((x86_cost - arm64_cost) / x86_cost) * 100
   Performance Gain % = ((x86_time - arm64_time) / x86_time) * 100
   ```

### Demo Script

1. **Deploy both architectures**: `.\deploy-all.ps1 -ArchitectureType both`
2. **Run x86_64 tests first**: Show baseline performance
3. **Run ARM64 tests**: Demonstrate improvements
4. **Show side-by-side comparison**: Use visualization URLs
5. **Highlight cost savings**: Emphasize 20% reduction
6. **Discuss use cases**: When to choose each architecture

## Key Takeaways

| Workload Type | ARM64 Advantage | Recommended Choice |
|---------------|-----------------|-------------------|
| **CPU-Intensive** | Highest (performance + cost) | **ARM64** |
| **I/O-Bound** | Cost only (~20%) | **ARM64** (for cost) |
| **Memory-Intensive** | Moderate (performance + cost) | **ARM64** |
| **Simple API** | Cost only (~20%) | **ARM64** (for cost) |

**Default Recommendation**: Use ARM64 unless you have specific dependencies that require x86_64.
