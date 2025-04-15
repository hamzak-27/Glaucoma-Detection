import os
import django
from django.db import connection
from django.core.management import call_command

def test_database():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glaucoma_detector.settings')
    django.setup()

    # Test database connection
    print("Testing database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return

    # Test if tables exist
    print("\nChecking tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cursor.fetchall()
            print(f"✓ Found {len(tables)} tables")
            for table in tables:
                print(f"  - {table[0]}")
    except Exception as e:
        print(f"✗ Error checking tables: {str(e)}")

if __name__ == '__main__':
    test_database() 