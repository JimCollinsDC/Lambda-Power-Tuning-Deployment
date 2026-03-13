import json
import time


def fibonacci(n):
    """Calculate Fibonacci number recursively (inefficient on purpose for CPU demo)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_primes(limit):
    """Find all prime numbers up to limit"""
    return [n for n in range(2, limit) if is_prime(n)]


def lambda_handler(event, context):
    """
    CPU-intensive Lambda function for power tuning demonstration.
    Performs Fibonacci calculations and prime number generation.
    """
    start_time = time.time()
    
    # Parse input parameters
    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    fib_n = body.get('fibonacci', 35)
    prime_limit = body.get('prime_limit', 10000)
    
    # Perform CPU-intensive operations
    results = {
        'fibonacci': {
            'n': fib_n,
            'result': fibonacci(fib_n)
        },
        'primes': {
            'limit': prime_limit,
            'count': len(find_primes(prime_limit)),
            'sample': find_primes(min(prime_limit, 100))[:10]  # First 10 primes as sample
        }
    }
    
    execution_time = time.time() - start_time
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'CPU-intensive operations completed',
            'results': results,
            'execution_time_seconds': round(execution_time, 3),
            'memory_allocated_mb': context.memory_limit_in_mb,
            'request_id': getattr(context, 'aws_request_id', getattr(context, 'request_id', None))
        })
    }
