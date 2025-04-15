"""
WSGI config for glaucoma_detector project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Add the project directory to the Python path
    BASE_DIR = Path(__file__).resolve().parent.parent
    sys.path.append(str(BASE_DIR))
    logger.info(f"Added {BASE_DIR} to Python path")

    # Set up Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glaucoma_detector.settings")
    logger.info("Set Django settings module")

    # Import Django after setting up environment
    from django.core.wsgi import get_wsgi_application
    logger.info("Imported Django WSGI application")

    # Initialize Django
    application = get_wsgi_application()
    logger.info("Initialized Django application")

except Exception as e:
    logger.error(f"Error initializing Django: {str(e)}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Current working directory: {os.getcwd()}")
    logger.error(f"Environment variables: {os.environ}")
    raise
