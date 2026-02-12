import os
import django
import random
from django.conf import settings
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'west_swiss_hotel.settings')
django.setup()

from bookings.models import Room, RoomImage

def populate_gallery():
    rooms = Room.objects.all()
    media_root = settings.MEDIA_ROOT
    rooms_dir = os.path.join(media_root, 'rooms')
    
    # Get potential images from media/rooms (excluding directories)
    if not os.path.exists(rooms_dir):
        print(f"Directory {rooms_dir} does not exist.")
        return

    available_images = [
        f for f in os.listdir(rooms_dir) 
        if os.path.isfile(os.path.join(rooms_dir, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    print(f"Found {len(available_images)} images in media/rooms/")

    if not available_images:
        print("No images found to use for gallery.")
        return

    for room in rooms:
        existing_images_count = room.images.count()
        print(f"Processing {room}: has {existing_images_count} gallery images.")
        
        target_count = 5
        needed = target_count - existing_images_count
        
        if needed > 0:
            # Pick random images to add
            images_to_add = random.choices(available_images, k=needed)
            
            for img_name in images_to_add:
                source_path = os.path.join(rooms_dir, img_name)
                
                # We need to copy the file effectively or just reference it
                # For ImageField, usually we open the file and save it to the new model instance
                with open(source_path, 'rb') as f:
                    image_file = File(f)
                    
                    # Create RoomImage
                    # Note: This will copy the file to 'rooms/gallery/' due to upload_to='rooms/gallery/'
                    ri = RoomImage(room=room, caption=f"Gallery view for {room.get_room_type_display()}")
                    ri.image.save(f"gallery_{img_name}", image_file, save=True)
                    print(f"  Added {img_name} to gallery for {room}")

if __name__ == '__main__':
    populate_gallery()
