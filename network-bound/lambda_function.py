import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import gzip
import io


def fetch_and_process_url(url_config):
    """
    Fetch URL and perform CPU-intensive processing on the response.
    This simulates network-bound workloads that also do computation.
    """
    url = url_config['url']
    process_data = url_config.get('process', True)
    
    try:
        start = time.time()
        
        # Fetch data
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            fetch_time = time.time() - start
            
            # Perform CPU-intensive processing on network data
            if process_data:
                # Decompress if gzipped
                try:
                    data = gzip.decompress(data)
                except:
                    pass
                
                # Calculate multiple hashes (CPU-intensive)
                hashes = {
                    'md5': hashlib.md5(data).hexdigest(),
                    'sha1': hashlib.sha1(data).hexdigest(),
                    'sha256': hashlib.sha256(data).hexdigest(),
                }
                
                # Count characters and analyze (CPU work)
                text = data.decode('utf-8', errors='ignore')
                analysis = {
                    'length': len(text),
                    'words': len(text.split()),
                    'unique_chars': len(set(text)),
                    'lines': text.count('\n')
                }
                
                process_time = time.time() - start - fetch_time
            else:
                hashes = {}
                analysis = {}
                process_time = 0
        
        return {
            'url': url,
            'success': True,
            'fetch_time': round(fetch_time, 3),
            'process_time': round(process_time, 3),
            'total_time': round(time.time() - start, 3),
            'data_size': len(data),
            'hashes': hashes,
            'analysis': analysis
        }
    
    except Exception as e:
        return {
            'url': url,
            'success': False,
            'error': str(e),
            'total_time': round(time.time() - start, 3)
        }


def lambda_handler(event, context):
    """
    Network-bound Lambda function for power tuning demonstration.
    Combines parallel network I/O with CPU-intensive processing.
    Benefits from 2 vCPUs (available at 1769+ MB memory).
    """
    start_time = time.time()
    
    # Parse input parameters
    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    num_requests = body.get('num_requests', 15)
    max_workers = body.get('max_workers', 10)
    
    # URLs that return substantial data for processing
    urls = [
        {'url': 'https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l', 'process': True},
        {'url': 'https://httpbin.org/json', 'process': True},
        {'url': 'https://httpbin.org/uuid', 'process': True},
        {'url': 'https://httpbin.org/headers', 'process': True},
        {'url': 'https://httpbin.org/html', 'process': True},
        {'url': 'https://httpbin.org/robots.txt', 'process': True},
        {'url': 'https://httpbin.org/anything', 'process': True},
        {'url': 'https://httpbin.org/stream/20', 'process': True},
    ]
    
    # Repeat URLs to match requested number
    urls_to_fetch = (urls * ((num_requests // len(urls)) + 1))[:num_requests]
    
    # Perform network + processing in parallel
    # With 2 vCPUs, this should show significant improvement
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_and_process_url, url_config): url_config for url_config in urls_to_fetch}
        
        for future in as_completed(future_to_url):
            results.append(future.result())
    
    # Calculate statistics
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    stats = {
        'total_requests': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'total_bytes': sum(r.get('data_size', 0) for r in successful),
        'avg_fetch_time': round(sum(r.get('fetch_time', 0) for r in successful) / len(successful), 3) if successful else 0,
        'avg_process_time': round(sum(r.get('process_time', 0) for r in successful) / len(successful), 3) if successful else 0,
        'avg_total_time': round(sum(r.get('total_time', 0) for r in successful) / len(successful), 3) if successful else 0,
    }
    
    execution_time = time.time() - start_time
    
    # Determine vCPU allocation based on memory
    memory_mb = context.memory_limit_in_mb
    vcpu_count = 2 if memory_mb >= 1769 else round(memory_mb / 1769, 2)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Network-bound operations with processing completed',
            'statistics': stats,
            'execution_time_seconds': round(execution_time, 3),
            'function_info': {
                'memory_allocated_mb': memory_mb,
                'estimated_vcpu': vcpu_count,
                'vcpu_note': '2 full vCPUs available at 1769+ MB',
                'request_id': context.aws_request_id
            },
            'note': 'This function benefits from 2 vCPUs for parallel network I/O + CPU processing',
            'sample_results': results[:3]  # First 3 results as sample
        })
    }
