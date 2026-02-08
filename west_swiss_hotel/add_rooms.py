import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'west_swiss_hotel.settings')
django.setup()

from bookings.models import Room

def add_rooms():
    rooms_data = [
        {
            'room_type': 'STANDARD',
            'price_per_night': 35000,
            'view_type': 'City View',
            'description': 'A comfortable and well-appointed standard room featuring a queen-sized bed, perfect for business or leisure.',
            'image': 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?q=80&w=1974&auto=format&fit=crop',
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True
        },
        {
            'room_type': 'DELUXE',
            'price_per_night': 55000,
            'view_type': 'Pool View',
            'description': 'Our spacious deluxe suites offer a touch of luxury with king-sized beds, stunning pool views, and extra seating areas.',
            'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?q=80&w=1974&auto=format&fit=crop',
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True
        },
        {
            'room_type': 'EXECUTIVE',
            'price_per_night': 85000,
            'view_type': 'Panoramic View',
            'description': 'Experience the ultimate in comfort with our executive king rooms. High-floor placement provides breathtaking views of Aba.',
            'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4df85b?q=80&w=2070&auto=format&fit=crop',
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True
        },
        {
            'room_type': 'STANDARD',
            'price_per_night': 38000,
            'view_type': 'Garden View',
            'description': 'Quiet and serene standard room overlooking our private gardens. Features sleek modern decor.',
            'image': 'https://images.unsplash.com/photo-1505691938895-1758d7eaa511?q=80&w=2070&auto=format&fit=crop',
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True
        },
        {
            'room_type': 'DELUXE',
            'price_per_night': 60000,
            'view_type': 'City Skyline',
            'description': 'Elevated deluxe living with a focus on design and comfort. Includes a mini-bar and premium coffee maker.',
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?q=80&w=2070&auto=format&fit=crop',
            'has_wifi': True,
            'has_breakfast': True,
            'has_ac': True
        }
    ]

    print(f"Adding {len(rooms_data)} rooms to the database...")
    
    for room_info in rooms_data:
        room, created = Room.objects.get_or_create(
            description=room_info['description'],
            defaults=room_info
        )
        if created:
            print(f"Created: {room.get_room_type_display()} - {room.view_type}")
        else:
            print(f"Skipped (already exists): {room.get_room_type_display()} - {room.view_type}")

if __name__ == "__main__":
    add_rooms()
    print("Done!")
