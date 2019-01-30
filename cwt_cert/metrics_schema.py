schema = {
    'type': 'object',
    'properties': {
        'health': {
            'type': 'object',
            'properties': {
                'user_jobs_queued': {'type': 'number'},
                'user_jobs_running': {'type': 'number'},
                'cpu_avg': {'type': 'number'},
                'memory_usage': {'type': 'number'},
                'wps_requests': {'type': 'number'},
                'memory_usage_avg_5m': {'type': 'number'},
                'cpu_count': {'type': 'number'},
                'memory_available': {'type': 'number'},
                'wps_requests_avg_5m': {'type': 'number'},
            }
        },
        'time': {
            'type': 'string',
        }
    }
}
