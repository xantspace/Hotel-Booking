import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'west_swiss_hotel.settings')
django.setup()

from bookings.models import Room, OTARate

def seed():
    # Rooms
    rooms_data = [
        {
            'room_type': 'STANDARD',
            'price_per_night': 80500,
            'view_type': 'Pool View',
            'description': 'Comfortable for solo or couples'
        },
        {
            'room_type': 'DELUXE',
            'price_per_night': 115000,
            'view_type': 'City View',
            'description': 'Spacious with premium city views'
        },
        {
            'room_type': 'EXECUTIVE',
            'price_per_night': 95000,
            'view_type': 'City View',
            'description': 'Ideal for business travellers'
        }
    ]

    for data in rooms_data:
        Room.objects.get_or_create(
            room_type=data['room_type'],
            defaults={
                'price_per_night': data['price_per_night'],
                'view_type': data['view_type'],
                'description': data['description']
            }
        )

    # OTA Rates
    ota_data = [
        {'name': 'Expedia.com', 'price': 114162, 'inclusions': 'Free breakfast • Free Wi-Fi'},
        {'name': 'ZenHotels.com', 'price': 126831, 'inclusions': 'Free breakfast'},
        {'name': 'Hotels.ng', 'price': 112750, 'inclusions': 'Standard Inclusions'},
        {'name': 'Bluepillow.com', 'price': 114162, 'inclusions': 'Free cancellation until 8 Feb'}
    ]

    for data in ota_data:
        OTARate.objects.get_or_create(
            platform_name=data['name'],
            defaults={
                'price': data['price'],
                'inclusions': data['inclusions']
            }
        )

    print("Data seeded successfully!")

if __name__ == '__main__':
    seed()
