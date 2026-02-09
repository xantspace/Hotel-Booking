from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('contact/', views.contact_view, name='contact'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    
    # Custom Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/rooms/', views.admin_rooms, name='admin_rooms'),
    path('admin/rooms/add/', views.add_room, name='add_room'),
    path('admin/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('admin/revenue/', views.admin_revenue, name='admin_revenue'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),
    path('admin/booking/<int:booking_id>/status/', views.update_booking_status, name='update_booking_status'),
    path('admin/messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]



