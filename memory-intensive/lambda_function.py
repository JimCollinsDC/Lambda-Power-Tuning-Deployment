import json
import time
import random


def generate_large_dataset(size_mb):
    """Generate a large dataset in memory"""
    # Each dict entry is roughly 100 bytes
    entries_per_mb = 10000
    num_entries = size_mb * entries_per_mb
    
    dataset = []
    for i in range(num_entries):
        dataset.append({
            'id': i,
            'value': random.random() * 1000,
            'category': f'category_{i % 100}',
            'timestamp': time.time(),
            'metadata': {
                'processed': False,
                'score': random.randint(1, 100),
                'tags': [f'tag_{j}' for j in range(5)]
            }
        })
    
    return dataset


def process_dataset(dataset, threshold):
    """Process the dataset with memory-intensive operations"""
    # Filter data
    filtered = [item for item in dataset if item['value'] > threshold]
    
    # Sort by value
    sorted_data = sorted(filtered, key=lambda x: x['value'], reverse=True)
    
    # Group by category
    grouped = {}
    for item in sorted_data:
        category = item['category']
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    
    # Calculate statistics per category
    stats = {}
    for category, items in grouped.items():
        values = [item['value'] for item in items]
        if values:
            stats[category] = {
                'count': len(values),
                'sum': sum(values),
                'average': sum(values) / len(values),
                'min': min(values),
                'max': max(values)
            }
    
    return sorted_data[:100], stats  # Return top 100 items and stats


def lambda_handler(event, context):
    """
    Memory-intensive Lambda function for power tuning demonstration.
    Processes large datasets in memory.
    """
    start_time = time.time()
    
    # Parse input parameters
    body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    data_size_mb = body.get('data_size_mb', 50)  # Default 50MB dataset
    threshold = body.get('threshold', 500)
    
    # Ensure data size doesn't exceed reasonable limits
    data_size_mb = min(data_size_mb, 200)
    
    # Generate large dataset
    generation_start = time.time()
    dataset = generate_large_dataset(data_size_mb)
    generation_time = time.time() - generation_start
    
    # Process dataset
    processing_start = time.time()
    top_items, category_stats = process_dataset(dataset, threshold)
    processing_time = time.time() - processing_start
    
    execution_time = time.time() - start_time
    
    # Calculate memory usage estimate
    dataset_size_bytes = len(json.dumps(dataset[:100]).encode('utf-8')) * (len(dataset) / 100)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Memory-intensive operations completed',
            'results': {
                'dataset_entries': len(dataset),
                'filtered_entries': len(top_items),
                'categories_found': len(category_stats),
                'sample_stats': dict(list(category_stats.items())[:5])  # First 5 categories
            },
            'timing': {
                'generation_time_seconds': round(generation_time, 3),
                'processing_time_seconds': round(processing_time, 3),
                'total_execution_time_seconds': round(execution_time, 3)
            },
            'memory_info': {
                'allocated_mb': context.memory_limit_in_mb,
                'estimated_dataset_size_mb': round(dataset_size_bytes / (1024 * 1024), 2)
            },
            'request_id': context.aws_request_id,
            'note': 'This function benefits from adequate memory allocation'
        })
    }
