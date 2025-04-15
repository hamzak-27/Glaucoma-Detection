import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glaucoma_detector.settings")

# Import Django after setting up environment
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Initialize Django
django_app = get_wsgi_application()

# Wrap with WhiteNoise for static files
application = WhiteNoise(django_app, root=os.path.join(BASE_DIR, 'staticfiles'))
application.add_files(os.path.join(BASE_DIR, 'static'), prefix='static/')

# Vercel requires a handler function
def handler(event, context):
    return application(event, context) 