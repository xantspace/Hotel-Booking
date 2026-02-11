from django.db import models
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    class RoomType(models.TextChoices):
        STANDARD = 'STANDARD', _('Standard Room')
        DELUXE = 'DELUXE', _('Deluxe Suite')
        EXECUTIVE = 'EXECUTIVE', _('Executive King')
        PRESIDENTIAL = 'PRESIDENTIAL', _('Presidential Suite')

    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.STANDARD)
    total_inventory = models.PositiveIntegerField(default=1, help_text="Total number of rooms of this type")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    view_type = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Pool View, City View")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, help_text="Main room image")

    # Core amenities
    has_wifi = models.BooleanField(default=True)
    has_breakfast = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=True)
    
    def get_available_inventory(self, check_in, check_out):
        """Returns the number of available rooms for given dates"""
        overlapping_bookings = self.bookings.filter(
            status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).count()
        return max(0, self.total_inventory - overlapping_bookings)

    def is_available(self, check_in, check_out):
        """Returns True if there is at least one room available"""
        return self.get_available_inventory(check_in, check_out) > 0

    def __str__(self):
        return f"{self.get_room_type_display()} - ₦{self.price_per_night}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/gallery/')
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.room.get_room_type_display()}"

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        CHECKED_IN = 'CHECKED_IN', _('Checked In')
        COMPLETED = 'COMPLETED', _('Completed')

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.IntegerField(default=1)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    special_requests = models.TextField(blank=True, null=True)

    @property
    def display_id(self):
        return f"WSH{self.id:03d}"

    def __str__(self):
        return f"Booking #{self.display_id} - {self.guest_name}"

class OTARate(models.Model):
    platform_name = models.CharField(max_length=100, help_text="e.g. Expedia, Hotels.ng")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(blank=True, null=True)
    inclusions = models.CharField(max_length=255, blank=True, help_text="e.g. Free Breakfast, Free Wi-Fi")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OTA Rate"
        verbose_name_plural = "OTA Rates"

    def __str__(self):
        return f"{self.platform_name}: ₦{self.price}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
