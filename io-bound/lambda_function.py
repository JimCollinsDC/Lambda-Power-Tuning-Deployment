import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor


def fetch_url(url):
    """Fetch content from a URL"""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return {
                'url': url,
                'status': response.status,
                'length': len(response.read()),
                'success': True
            }
    except urllib.error.URLError as e:
        return {
            'url': url,
            'error': str(e),
            'success': False
        }


def lambda_handler(event, context):
    """
    I/O-bound Lambda function for power tuning demonstration.
    Makes multiple HTTP requests to demonstrate I/O-bound workloads.
    """
    start_time = time.time()
    
    # Parse input parameters
    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    num_requests = body.get('num_requests', 10)
    
    # Default URLs to fetch (using httpbin for testing)
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/uuid',
        'https://httpbin.org/json',
        'https://httpbin.org/headers',
        'https://httpbin.org/ip',
    ]
    
    # Repeat URLs to match requested number
    urls_to_fetch = (urls * ((num_requests // len(urls)) + 1))[:num_requests]
    
    # Perform I/O operations in parallel
    with ThreadPoolExecutor(max_workers=min(num_requests, 10)) as executor:
        results = list(executor.map(fetch_url, urls_to_fetch))
    
    # Calculate statistics
    successful = sum(1 for r in results if r.get('success'))
    failed = len(results) - successful
    total_bytes = sum(r.get('length', 0) for r in results if r.get('success'))
    
    execution_time = time.time() - start_time
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'I/O-bound operations completed',
            'statistics': {
                'total_requests': len(results),
                'successful': successful,
                'failed': failed,
                'total_bytes_fetched': total_bytes
            },
            'execution_time_seconds': round(execution_time, 3),
            'memory_allocated_mb': context.memory_limit_in_mb,
            'request_id': getattr(context, 'aws_request_id', getattr(context, 'request_id', None)),
            'note': 'I/O-bound functions typically show minimal improvement with higher memory allocation'
        })
    }
