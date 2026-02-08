from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('contact/', views.contact_view, name='contact'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]

