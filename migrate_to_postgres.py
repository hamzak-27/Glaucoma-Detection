import os
import json
import django
from django.core.management import call_command
from django.db import connection
import dj_database_url

def migrate_to_postgres():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glaucoma_detector.settings')
    django.setup()

    # Configure the database using DATABASE_URL
    db_config = dj_database_url.config(default=os.getenv('DATABASE_URL'))
    
    # First, ensure we're using the PostgreSQL database
    if connection.vendor != 'postgresql':
        print("Error: Not connected to PostgreSQL database")
        return

    # Run migrations
    print("Running migrations...")
    call_command('migrate')

    # Load the data
    print("Loading data from backup...")
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            # Load the data
            call_command('loaddata', 'data.json')
        print("Data migration completed successfully!")
    except Exception as e:
        print(f"Error during data migration: {str(e)}")

if __name__ == '__main__':
    migrate_to_postgres() 