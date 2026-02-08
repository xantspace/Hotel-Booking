import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'west_swiss_hotel.settings')
django.setup()

print("Making migrations...")
call_command('makemigrations', 'bookings')
print("Migrating...")
call_command('migrate')
print("Seeding...")
# Seed data logic from seed_hotel_data.py if possible, or just call it
try:
    import seed_hotel_data
    print("Seed data script executed.")
except Exception as e:
    print(f"Error seeding: {e}")
