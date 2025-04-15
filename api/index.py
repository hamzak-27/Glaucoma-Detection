import os
import sys
import json
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glaucoma_detector.settings")

try:
    # Import Django after setting up environment
    from django.core.wsgi import get_wsgi_application
    from django.http import HttpResponse
    from django.urls import get_resolver
    from django.conf import settings
    
    # Initialize Django
    django_app = get_wsgi_application()
    
    def handler(event, context):
        try:
            # Get the path from the event
            path = event.get('path', '/')
            
            # Create a Django request
            from django.core.handlers.wsgi import WSGIRequest
            from io import BytesIO
            from urllib.parse import parse_qs
            
            body = event.get('body', '')
            headers = event.get('headers', {})
            method = event.get('httpMethod', 'GET')
            
            # Create WSGI environment
            environ = {
                'REQUEST_METHOD': method,
                'PATH_INFO': path,
                'QUERY_STRING': event.get('queryStringParameters', {}),
                'wsgi.input': BytesIO(body.encode() if body else b''),
                'wsgi.url_scheme': 'https',
                'SERVER_NAME': headers.get('host', ''),
                'SERVER_PORT': '443',
                'CONTENT_TYPE': headers.get('content-type', ''),
                'CONTENT_LENGTH': str(len(body.encode() if body else b'')),
            }
            
            # Add headers to environ
            for key, value in headers.items():
                key = 'HTTP_' + key.upper().replace('-', '_')
                environ[key] = value
            
            # Create request
            request = WSGIRequest(environ)
            
            # Get response
            response = django_app(request)
            
            # Convert response to API Gateway format
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.content.decode('utf-8')
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': f'Error: {str(e)}'
            }
            
except Exception as e:
    def handler(event, context):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Django initialization error: {str(e)}'
        } 