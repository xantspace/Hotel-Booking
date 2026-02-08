import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'west_swiss_hotel.settings')
django.setup()

from bookings.models import Room, OTARate

# Check current rooms
print("=" * 50)
print("CURRENT DATABASE STATUS")
print("=" * 50)

room_count = Room.objects.count()
print(f"\nTotal Rooms in DB: {room_count}")

if room_count == 0:
    print("\n⚠️  No rooms found! Creating rooms now...")
    
    # Create rooms
    rooms_data = [
        {
            'room_type': 'STANDARD',
            'price_per_night': 80500,
            'view_type': 'Pool View',
            'description': 'Comfortable for solo or couples',
            'is_available': True,
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True,
        },
        {
            'room_type': 'DELUXE',
            'price_per_night': 115000,
            'view_type': 'City View',
            'description': 'Spacious with premium city views',
            'is_available': True,
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True,
        },
        {
            'room_type': 'EXECUTIVE',
            'price_per_night': 95000,
            'view_type': 'City View',
            'description': 'Ideal for business travellers',
            'is_available': True,
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True,
        }
    ]

    for data in rooms_data:
        room = Room.objects.create(**data)
        print(f"✅ Created: {room.get_room_type_display()} - ₦{room.price_per_night:,}")

else:
    print("\nExisting rooms:")
    for room in Room.objects.all():
        status = "✅ Available" if room.is_available else "❌ Not Available"
        print(f"  {room.id}. {room.get_room_type_display()} - ₦{room.price_per_night:,} - {status}")

# Check OTA rates
print("\n" + "=" * 50)
ota_count = OTARate.objects.count()
print(f"Total OTA Rates in DB: {ota_count}")

if ota_count == 0:
    print("\n⚠️  No OTA rates found! Creating rates now...")
    
    ota_data = [
        {'platform_name': 'Expedia.com', 'price': 114162, 'inclusions': 'Free breakfast • Free Wi-Fi'},
        {'platform_name': 'ZenHotels.com', 'price': 126831, 'inclusions': 'Free breakfast'},
        {'platform_name': 'Hotels.ng', 'price': 112750, 'inclusions': 'Standard Inclusions'},
        {'platform_name': 'Bluepillow.com', 'price': 114162, 'inclusions': 'Free cancellation until 8 Feb'}
    ]

    for data in ota_data:
        rate = OTARate.objects.create(**data)
        print(f"✅ Created: {rate.platform_name} - ₦{rate.price:,}")
else:
    print("\nExisting OTA rates:")
    for rate in OTARate.objects.all():
        print(f"  {rate.platform_name}: ₦{rate.price:,}")

print("\n" + "=" * 50)
print("DATABASE SETUP COMPLETE!")
print("=" * 50)
