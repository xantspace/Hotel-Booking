from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Room, Booking, OTARate

# Custom Admin Site
class WestSwissAdminSite(admin.AdminSite):
    site_header = "West-Swiss Hotel Administration"
    site_title = "Hotel Admin"
    index_title = "Hotel Management Dashboard"
    index_template = 'admin/index.html'
    
    def index(self, request, extra_context=None):
        """Custom admin index with dashboard statistics"""
        # Date ranges
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        next_month = (this_month_start + timedelta(days=32)).replace(day=1)
        
        # Booking statistics
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='PENDING').count()
        confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
        checked_in = Booking.objects.filter(status='CHECKED_IN').count()
        
        # Revenue statistics
        total_revenue = Booking.objects.filter(
            status__in=['CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        this_month_revenue = Booking.objects.filter(
            status__in=['CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT'],
            created_at__gte=this_month_start
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Recent bookings
        recent_bookings = Booking.objects.select_related('room').order_by('-created_at')[:10]
        
        # Upcoming check-ins
        upcoming_checkins = Booking.objects.filter(
            check_in__gte=today,
            check_in__lte=today + timedelta(days=7),
            status__in=['PENDING', 'CONFIRMED']
        ).select_related('room').order_by('check_in')[:10]
        
        # Current guests
        current_guests = Booking.objects.filter(
            status='CHECKED_IN'
        ).select_related('room').order_by('check_out')
        
        # Room availability
        total_capacity = Room.objects.aggregate(total=Sum('total_inventory'))['total'] or 0
        current_bookings_count = Booking.objects.filter(
            status__in=['CONFIRMED', 'CHECKED_IN'],
            check_in__lte=today,
            check_out__gt=today
        ).count()
        available_rooms = max(0, total_capacity - current_bookings_count)
        occupancy_rate = (current_bookings_count / total_capacity * 100) if total_capacity > 0 else 0
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'checked_in': checked_in,
            'total_revenue': total_revenue,
            'this_month_revenue': this_month_revenue,
            'recent_bookings': recent_bookings,
            'upcoming_checkins': upcoming_checkins,
            'current_guests': current_guests,
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'occupancy_rate': round(occupancy_rate, 1),
        })
        
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = WestSwissAdminSite(name='westswiss_admin')

class RoomImageInline(admin.TabularInline):
    model = Room.images.rel.related_model
    extra = 5

@admin.register(Room, site=admin_site)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type_badge', 'view_type', 'price_display', 'total_inventory', 'get_current_availability', 'amenities_display')
    list_filter = ('room_type', 'view_type', 'has_wifi', 'has_breakfast', 'has_ac')
    search_fields = ('description',)
    list_editable = ('total_inventory',)
    inlines = [RoomImageInline]
    actions = ['increase_price_5', 'decrease_price_5']
    
    def room_type_badge(self, obj):
        colors = {
            'STANDARD': '#10b981',
            'DELUXE': '#3b82f6',
            'EXECUTIVE': '#8b5cf6',
            'PRESIDENTIAL': '#f43f5e',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.room_type, '#6b7280'),
            obj.get_room_type_display()
        )
    room_type_badge.short_description = 'Room Type'
    
    def price_display(self, obj):
        price_str = f'{obj.price_per_night:,.0f}'
        return format_html('₦{}', price_str)
    price_display.short_description = 'Price/Night'
    price_display.admin_order_field = 'price_per_night'
    
    def get_current_availability(self, obj):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        avail = obj.get_available_inventory(today, tomorrow)
        color = '#10b981' if avail > 0 else '#ef4444'
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {} / {} Free</span>',
            color, avail, obj.total_inventory
        )
    get_current_availability.short_description = 'Available Today'
    
    def amenities_display(self, obj):
        amenities = []
        if obj.has_wifi:
            amenities.append('WiFi')
        if obj.has_breakfast:
            amenities.append('Breakfast')
        if obj.has_ac:
            amenities.append('AC')
        return ', '.join(amenities) if amenities else 'None'
    amenities_display.short_description = 'Amenities'
    
    
    def increase_price_5(self, request, queryset):
        for room in queryset:
            room.price_per_night *= 1.05
            room.save()
        self.message_user(request, f'{queryset.count()} room(s) price increased by 5 percent.')
    increase_price_5.short_description = "Increase price by 5 percent"
    
    def decrease_price_5(self, request, queryset):
        for room in queryset:
            room.price_per_night *= 0.95
            room.save()
        self.message_user(request, f'{queryset.count()} room(s) price decreased by 5 percent.')
    decrease_price_5.short_description = "Decrease price by 5 percent"

@admin.register(Booking, site=admin_site)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'guest_name_link', 'room_info', 'dates_display', 'status_badge', 'total_price_display', 'created_display')
    list_filter = ('status', 'check_in', 'check_out', 'room__room_type', 'created_at')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'id')
    date_hierarchy = 'check_in'
    readonly_fields = ('created_at', 'booking_summary')
    actions = ['approve_bookings', 'mark_checked_in', 'mark_checked_out', 'cancel_bookings']
    
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_summary',)
        }),
        ('Booking Information', {
            'fields': ('room', 'check_in', 'check_out', 'number_of_guests', 'status')
        }),
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone', 'special_requests')
        }),
        ('Payment Information', {
            'fields': ('total_price',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def booking_ref(self, obj):
        return f'#{obj.display_id}'
    booking_ref.short_description = 'Ref'
    
    def guest_name_link(self, obj):
        return format_html('<strong>{}</strong><br><small style="color: #6b7280;">{}</small>', 
                         obj.guest_name, obj.guest_email)
    guest_name_link.short_description = 'Guest'
    
    def room_info(self, obj):
        return format_html('{}<br><small style="color: #6b7280;">{}</small>', 
                         obj.room.get_room_type_display(), obj.room.view_type)
    room_info.short_description = 'Room'
    
    def dates_display(self, obj):
        num_nights = (obj.check_out - obj.check_in).days
        return format_html(
            '{}<br><small style="color: #6b7280;">to {}</small><br><small style="color: #10b981;">{} night{}</small>',
            obj.check_in.strftime('%b %d, %Y'),
            obj.check_out.strftime('%b %d, %Y'),
            num_nights,
            's' if num_nights != 1 else ''
        )
    dates_display.short_description = 'Stay Period'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#f59e0b',
            'CONFIRMED': '#10b981',
            'CHECKED_IN': '#3b82f6',
            'CHECKED_OUT': '#6b7280',
            'CANCELLED': '#ef4444',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def total_price_display(self, obj):
        price_str = f'{obj.total_price:,.0f}'
        return format_html('<strong style="color: #0d5c5c;">₦{}</strong>', price_str)
    total_price_display.short_description = 'Total'
    total_price_display.admin_order_field = 'total_price'
    
    def created_display(self, obj):
        return obj.created_at.strftime('%b %d, %Y %H:%M')
    created_display.short_description = 'Booked On'
    created_display.admin_order_field = 'created_at'
    
    def booking_summary(self, obj):
        num_nights = (obj.check_out - obj.check_in).days
        return format_html(
            '<div style="background: #f3f4f6; padding: 16px; border-radius: 8px;">'
            '<h3 style="margin-top: 0;">Booking #{}</h3>'
            '<p><strong>Guest:</strong> {} ({})</p>'
            '<p><strong>Room:</strong> {}</p>'
            '<p><strong>Duration:</strong> {} nights ({} to {})</p>'
            '<p><strong>Guests:</strong> {}</p>'
            '<p><strong>Total:</strong> ₦{}</p>'
            '</div>',
            obj.display_id,
            obj.guest_name, obj.guest_email,
            obj.room.get_room_type_display(),
            num_nights, obj.check_in.strftime('%B %d, %Y'), obj.check_out.strftime('%B %d, %Y'),
            obj.number_of_guests,
            f'{obj.total_price:,.0f}'
        )
    booking_summary.short_description = 'Summary'
    
    def approve_bookings(self, request, queryset):
        updated = queryset.filter(status='PENDING').update(status='CONFIRMED')
        self.message_user(request, f'{updated} booking(s) confirmed.')
    approve_bookings.short_description = "Approve selected bookings"
    
    def mark_checked_in(self, request, queryset):
        updated = queryset.filter(status='CONFIRMED').update(status='CHECKED_IN')
        self.message_user(request, f'{updated} guest(s) marked as checked in.')
    mark_checked_in.short_description = "Mark as checked in"
    
    def mark_checked_out(self, request, queryset):
        updated = queryset.filter(status='CHECKED_IN').update(status='CHECKED_OUT')
        self.message_user(request, f'{updated} guest(s) marked as checked out.')
    mark_checked_out.short_description = "Mark as checked out"
    
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f'{updated} booking(s) cancelled.')
    cancel_bookings.short_description = "Cancel selected bookings"

@admin.register(OTARate, site=admin_site)
class OTARateAdmin(admin.ModelAdmin):
    list_display = ('platform_badge', 'price', 'price_display', 'inclusions', 'last_updated_display')
    list_filter = ('platform_name', 'last_updated')
    search_fields = ('platform_name', 'inclusions')
    readonly_fields = ('last_updated',)
    list_editable = ('price',)
    
    def platform_badge(self, obj):
        return format_html(
            '<span style="background-color: #0d5c5c; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            obj.platform_name
        )
    platform_badge.short_description = 'Platform'
    
    def price_display(self, obj):
        price_str = f'{obj.price:,.0f}'
        return format_html('₦{}', price_str)
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    
    def last_updated_display(self, obj):
        return obj.last_updated.strftime('%b %d, %Y %H:%M')
    last_updated_display.short_description = 'Last Updated'
    last_updated_display.admin_order_field = 'last_updated'
