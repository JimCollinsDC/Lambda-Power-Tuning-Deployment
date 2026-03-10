import json
import time
from datetime import datetime


def lambda_handler(event, context):
    """
    Simple API Lambda function for power tuning demonstration.
    Provides basic REST API functionality as a baseline comparison.
    """
    start_time = time.time()
    
    # Parse request
    http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'GET'))
    path = event.get('path', event.get('rawPath', '/'))
    
    # Simple routing
    if path == '/' or path == '/health':
        response_data = {
            'status': 'healthy',
            'message': 'Simple API Lambda function is running',
            'timestamp': datetime.utcnow().isoformat(),
            'function_info': {
                'memory_allocated_mb': context.memory_limit_in_mb,
                'request_id': context.aws_request_id,
                'remaining_time_ms': context.get_remaining_time_in_millis()
            }
        }
    
    elif path == '/echo':
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
        response_data = {
            'message': 'Echo response',
            'received': body,
            'method': http_method,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    elif path == '/info':
        response_data = {
            'function_name': context.function_name,
            'function_version': context.function_version,
            'memory_limit_mb': context.memory_limit_in_mb,
            'log_group_name': context.log_group_name,
            'log_stream_name': context.log_stream_name,
            'request_id': context.aws_request_id,
            'aws_request_id': context.aws_request_id,
            'invoked_function_arn': context.invoked_function_arn
        }
    
    else:
        execution_time = time.time() - start_time
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Not Found',
                'path': path,
                'execution_time_seconds': round(execution_time, 3)
            })
        }
    
    execution_time = time.time() - start_time
    response_data['execution_time_seconds'] = round(execution_time, 3)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'X-Execution-Time': str(execution_time)
        },
        'body': json.dumps(response_data)
    }
