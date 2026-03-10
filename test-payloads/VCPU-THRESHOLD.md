# Network-Bound Function - 2 vCPU Threshold Testing

This function demonstrates the performance benefit of crossing the **2 vCPU threshold at 1769 MB memory**.

## Lambda vCPU Allocation

| Memory (MB) | vCPU Allocation |
|-------------|-----------------|
| 128 - 1768  | Fractional (proportional to memory) |
| **1769**    | **1 full vCPU** |
| **1770 - 3536** | **Proportional to 2 vCPUs** |
| **3537+**   | **2 full vCPUs** |

## Network-Bound vs I/O-Bound

- **I/O-Bound**: Simple HTTP requests, mostly waiting (doesn't benefit much from more CPU)
- **Network-Bound**: Network I/O + CPU processing (hash calculations, data parsing) - benefits significantly from 2 vCPUs

## Test Configuration - Showing 2 Core Benefit

### Standard Configuration (x86_64)
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-network-bound",
  "powerValues": [512, 1024, 1536, 1769, 2048, 2560, 3008, 3537, 4096],
  "num": 10,
  "payload": {
    "num_requests": 15,
    "max_workers": 10
  },
  "parallelInvocation": true,
  "strategy": "balanced"
}
```

### ARM64 Configuration
```json
{
  "lambdaARN": "arn:aws:lambda:REGION:ACCOUNT:function:power-tuning-demo-network-bound-arm64",
  "powerValues": [512, 1024, 1536, 1769, 2048, 2560, 3008, 3537, 4096],
  "num": 10,
  "payload": {
    "num_requests": 15,
    "max_workers": 10
  },
  "parallelInvocation": true,
  "strategy": "balanced"
}
```

## What to Look For

### Performance Jumps
Watch for performance improvements at these thresholds:
- **1769 MB**: Gets 1 full vCPU (noticeable improvement from 1536 MB)
- **3537+ MB**: Gets 2 full vCPUs (significant improvement for parallel workloads)

### Cost vs Performance Sweet Spots
- Below 1769 MB: Poor performance, not worth the savings
- 1769 - 2048 MB: Good balance for lighter workloads
- 2048 - 3008 MB: Better for moderate parallelism
- 3008+ MB: Best for heavy parallel network + CPU work

## Expected Results

### x86_64
| Memory | vCPU | Expected Time | Cost Level |
|--------|------|---------------|------------|
| 512    | ~0.29 | Slow (~15-20s) | Low |
| 1024   | ~0.58 | Moderate (~10-12s) | Medium-Low |
| 1536   | ~0.87 | Better (~7-9s) | Medium |
| **1769** | **1.0** | **Good (~5-7s)** | **Medium** |
| 2048   | ~1.16 | Better (~4-6s) | Medium-High |
| 3008   | ~1.70 | Fast (~3-4s) | High |
| **3537+** | **2.0** | **Fastest (~2-3s)** | **Highest** |

### ARM64
- ~20% faster at same memory levels
- ~20% cheaper at same memory levels
- Same vCPU threshold behaviors
- Better price/performance overall

## Demo Script

1. **Start with low memory** (512 MB):
   - Show slow performance
   - Explain fractional vCPU allocation

2. **Show 1769 MB threshold**:
   - Highlight the jump in performance
   - Explain "1 full vCPU" allocation

3. **Show 3537 MB threshold**:
   - Demonstrate the power of 2 vCPUs
   - Highlight parallel processing benefits

4. **Compare costs**:
   - Show cost vs performance trade-offs
   - Identify optimal configuration

5. **Compare x86_64 vs ARM64**:
   - Same memory configs
   - Show ARM64 advantage

## Key Takeaways

- **Network + CPU workloads** benefit significantly from crossing vCPU thresholds
- **1769 MB** is the "magic number" for 1 full vCPU
- **3537+ MB** unlocks 2 full vCPUs for maximum parallelism
- **ARM64** provides better value at all memory levels
- **Pure I/O workloads** don't benefit as much (see io-bound function)

## Payload Options

### Light Load (fewer requests)
```json
{
  "num_requests": 8,
  "max_workers": 5
}
```

### Medium Load (default)
```json
{
  "num_requests": 15,
  "max_workers": 10
}
```

### Heavy Load (stress test)
```json
{
  "num_requests": 25,
  "max_workers": 15
}
```

## Technical Details

The function performs:
1. **Network I/O**: Parallel HTTP requests
2. **CPU Processing**: 
   - MD5, SHA1, SHA256 hash calculations
   - Text parsing and analysis
   - Character counting and statistics
3. **Concurrent execution**: Multiple threads processing simultaneously

This combination makes it ideal for demonstrating the benefit of additional vCPU capacity.
